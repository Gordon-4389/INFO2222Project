const crypto = require("crypto");

// // The `generateKeyPairSync` method accepts two arguments:
// // 1. The type ok keys we want, which in this case is "rsa"
// // 2. An object with the properties of the key
var keypair = require('keypair');

var pair = keypair();
var Key = {
  public_key : pair.public,
  private_key : pair.private
}

fs = require('fs');
fs.writeFile('public.txt', Key.public_key, function (err) {
    if (err) 
        return console.log(err);
    // console.log('Wrote Hello World in file helloworld.txt, just check it');
});
// var pub = Key.publicKey;

// let keyPair = await window.crypto.subtle.generateKey(
//     {
//       name: "RSA-OAEP",
//       modulusLength: 4096,
//       publicExponent: new Uint8Array([1, 0, 1]),
//       hash: "SHA-256"
//     },
//     true,
//     ["encrypt", "decrypt"]
//   );
// let keyPair = window.crypto.subtle.generateKey(
//   {
//     name: "RSA-OAEP",
//     modulusLength: 4096,
//     publicExponent: new Uint8Array([1, 0, 1]),
//     hash: "SHA-256"
//   },
//   true,
//   ["encrypt", "decrypt"]
// );
// const Key =
// {
//   public_key : keyPair.publicKey,
//   private_key : keyPair.privateKey
// };

// const car = {type:"Fiat", model:"500", color:"white"};
// const publicKey = keyPair.publicKey;
// await crypto.subtle.exportKey("jwk", keyPair.publicKey);
// const privateKey = keyPair.privateKey;
// await crypto.subtle.exportKey("jwk", keyPair.privateKey);









