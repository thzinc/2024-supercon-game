const mqtt = require("mqtt");
const client = mqtt.connect("mqtt://broker.emqx.io:1883");

const GAME_ID = "ceremony-demo";
const DEVICE_ID = `bot-${Math.round(Math.random() * 1000000000)}`;
const TOPIC_PREFIX = "thzinc/2024-supercon/game/" + GAME_ID;

client.on("connect", () => {
  console.debug("connected");
  client.subscribe(`${TOPIC_PREFIX}/#`, (err) => {
    if (err) {
      console.error(err);
    }
  });
});

console.debug("start");

function fire() {
  const row = Math.floor(Math.random() * 8) + 1;
  client.publish(
    `${TOPIC_PREFIX}/projectile/${DEVICE_ID}`,
    String.fromCharCode(row)
  );

  const sleep = Math.floor(Math.random() * 1000) + 250;
  setTimeout(fire, 500);
}

fire();
