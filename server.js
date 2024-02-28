const { MTProto } = require('telegram-mtproto');

// Initialize the Telegram MTProto client
const api = {
  layer: 57, // The layer version
  initConnection: 0x69796de9, // The initConnection value
  api_id: YOUR_API_ID, // Your api_id
  app_version: '1.0.0', // Your app version
  lang_code: 'en' // Your language code
};

const telegram = MTProto({ api });

// Authenticate and get access to the channel
telegram('channels.getMessages', {
  channel: '@channel_username', // Replace with the actual channel username
  id: [1], // Replace with the message IDs to retrieve
}).then((result) => {
  // Process the retrieved messages
  console.log(result);
}).catch((error) => {
  // Handle any errors
  console.error(error);
});