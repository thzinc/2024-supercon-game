from mqtt_as import MQTTClient, config
import asyncio
from struct import pack, unpack
from constants import WIFI_SSID, WIFI_PASSWORD, MQTT_HOST, GAME_ID, DEVICE_ID
import math

config["ssid"] = WIFI_SSID
config["wifi_pw"] = WIFI_PASSWORD
config["server"] = MQTT_HOST

TOPIC_PREFIX = "thzinc/2024-supercon/game/" + GAME_ID

player_row_set_mask = 0b01000000
player_row_reset_mask = 0b10111111

# State
rows = [0, 0, 0, 0, 0, 0, 0, 0]
sent_projectiles = [False, False, False, False, False, False, False, False]
projectiles = set()
clears = set()
player_row = 1
player_alive = True
left_down = False
right_down = False
fire_down = False


async def send_projectile(client, row):
    global projectiles
    global clears
    r = row - 1
    if sent_projectiles[r]:
        return

    sent_projectiles[r] = True

    ev = client.publish(
        TOPIC_PREFIX + "/projectile/" + DEVICE_ID, pack("B", row), qos=1
    )

    for col in range(7, 0, -1):
        projectiles.add((row, col))
        await asyncio.sleep(0.200)
        clears.add((row, col))

    await asyncio.gather(ev)

    sent_projectiles[r] = False


async def receive_projectile(row):
    global player_alive
    global projectiles
    global clears
    global player_row

    if not player_alive:
        return

    for col in range(1, 8):
        projectiles.add((row, col))
        await asyncio.sleep(0.200)
        clears.add((row, col))

    if row == player_row:
        await kill_player()


async def render_projectiles():
    global player_alive
    global rows
    global projectiles

    while True:
        curr_projectiles = projectiles.copy()
        curr_clears = clears.copy()
        projectiles.clear()
        clears.clear()

        # Apply new projectile positions
        while True:
            try:
                row, col = curr_clears.pop()
                r = row - 1
                c = col - 1
                projectile_mask = 1 << c
                if player_alive:
                    rows[r] &= 0b11111111 ^ projectile_mask
            except KeyError:
                break

        while True:
            try:
                row, col = curr_projectiles.pop()
                r = row - 1
                c = col - 1
                projectile_mask = 1 << c
                if player_alive:
                    rows[r] |= projectile_mask
            except KeyError:
                break

        await asyncio.sleep(0)


async def render_rows():
    global rows
    while True:
        for row in range(1, 9):
            r = row - 1
            cols = rows[r]
            petal_bus.writeto_mem(PETAL_ADDRESS, row, bytes([cols]))
        await asyncio.sleep(0)


async def kill_player():
    global player_alive
    global rows
    player_alive = False
    print("kill")
    for row in range(1, 9):
        r = row - 1
        rows[r] = 0b01111111

    # Make center LED red
    rows[3 - 1] = 0b11111111
    await asyncio.sleep(0)


async def reset_player():
    global player_alive
    global rows

    for row in range(1, 9):
        r = row - 1
        rows[r] = 0b00000000

    rows[4 - 1] = 0b10000000
    await asyncio.sleep(1)

    rows[4 - 1] = 0b00000000
    player_alive = True


async def player(client):
    global player_alive
    global rows
    global player_row
    global left_down
    global right_down
    global fire_down

    while True:
        player_row_movement = 0
        if buttonA.value():
            left_down = True
        else:
            if left_down and player_alive:

                player_row_movement += 1
            left_down = False

        if buttonC.value():
            right_down = True
        else:
            if right_down and player_alive:
                player_row_movement -= 1
            right_down = False

        player_row = ((player_row - 1 + player_row_movement) % 8) + 1

        if buttonB.value():
            fire_down = True
        else:
            if fire_down:
                if player_alive:
                    asyncio.create_task(send_projectile(client, player_row))
                else:
                    await reset_player()

            fire_down = False

        # Update display
        for row in range(1, 9):
            r = row - 1
            if row == player_row:
                rows[r] |= player_row_set_mask
            else:
                rows[r] &= player_row_reset_mask

        await asyncio.sleep(0)


async def messages(client):
    own_topic = TOPIC_PREFIX + "/projectile/" + DEVICE_ID
    async for topic, msg, retained in client.queue:
        if topic.decode() == own_topic:
            pass
        else:
            (row,) = unpack("B", msg)
            asyncio.create_task(receive_projectile(row))


async def up(client):
    while True:
        await client.up.wait()
        client.up.clear()
        await client.subscribe(
            TOPIC_PREFIX + "/projectile/#",
            1,
        )


async def connect(client):
    global rows
    rows[2 - 1] |= 0b10000000
    await client.connect()
    rows[2 - 1] &= 0b01111111
    rows[4 - 1] |= 0b10000000
    await asyncio.sleep(0.500)
    rows[4 - 1] &= 0b00000000


async def main(client):
    asyncio.create_task(render_projectiles())
    asyncio.create_task(render_rows())

    await connect(client)
    asyncio.create_task(player(client))
    asyncio.create_task(up(client))
    asyncio.create_task(messages(client))

    while True:
        await asyncio.sleep(5)


config["queue_len"] = 16
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()
