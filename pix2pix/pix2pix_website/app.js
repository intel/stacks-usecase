'use strict';
const express = require('express');
const path = require('path');
const indexRouter = require('./routes/index');
const usersRouter = require('./routes/users');
const dirTree = require("directory-tree");
const tree = dirTree("./public/images");
const bodyParser = require('body-parser');
const axios = require('axios');
const ip = require('ip');
const multer  = require('multer');
var i = 0;
var fs = require('fs');
var uploadDir = './public/uploads/';
var renderDir = '../rendered/'
var uploadsDir = "../uploads/";
var imagesDir = "../images/";

if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
}

if (!fs.existsSync("./public/rendered")) {
  fs.mkdirSync("./public/rendered");
}

// Used for receiving uploaded image data from the webapp
var upload = multer({ dest: uploadDir });
var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: false
}));

app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, 'public')));
app.use('/', indexRouter);
app.use('/users', usersRouter);

// Return a JSON object containing the paths for all the available pre-created images.
app.use('/getImgJSON', (req, res) => {
  i = 0;
  console.log("Got img folder JSON request i = " + i);
  res.json(tree);
});

// Command called by the webapp when it has an image it wants rendered. This should return
// an object with the request ID, the starting image path, rendered image path, and original
// image URL.
app.post('/render', upload.single('imgData'), function (req, res, next) {
console.log("i = " + i);
console.log(req.body.type);
var imgToRender;

if (req.body.type === "BUFFER") {
  // Strip off the leading info that isn't image data
  var origDataStr = req.body.origData.replace(/^data:image\/(png|jpg);base64,/, "");
  var dataStr = req.body.imgData.replace(/^data:image\/(png|jpg);base64,/, "");
  var origBuffer = new Buffer(origDataStr, 'base64');
  var buffer = new Buffer(dataStr, 'base64');
  // Write buffer to our temporary file
  var imgOrig = 'original' + i + '.png';
  var imgToRender = 'upload' + i + '.png';
  var finishedImg = 'rendered' + i + '.jpg';
  i = i < 11 ? i + 1 : 0;
  console.log("Writing to file " + imgToRender);

  // Save the original buffer to file
  fs.writeFile(uploadDir + imgOrig, origBuffer, function (err) {
    if (err) {
      console.log("ERROR WRITING FILE");
      return next(err);
    }
  });

  // Save the 256x256 buffer to file, this is the size pix2pix expects
  fs.writeFile(uploadDir + imgToRender, buffer, function (err) {
    if (err) {
      console.log("ERROR WRITING FILE");
      return next(err);
    }

    // Load the image we want to have rendered
    fs.readFile(uploadDir + imgToRender, function (err, imgdata ) {
      renderImage(imgdata).then((response) => {
        console.log("SUCCESS");
        var lines = response.data.split('\n');
        var imgStr = lines[lines.length - 2]; // Data we actually care about is in the second to last slot of the array
        var imgBuff =  Buffer.from(imgStr.substr(2).slice(0, -9), 'base64'); // Currently need to strip the extra b' and ending that Python adds
        fs.writeFile("./public/rendered/" + finishedImg, imgBuff, function (err) {
          if (err) {
            console.log("ERROR WRITING FILE");
            return next(err);
          }
          res.json({reqID: Number(req.body.reqID), origPath: uploadsDir + imgOrig, startPath: uploadsDir + imgToRender, renderedPath: "../rendered/" + finishedImg});
          res.end('Rendering finished');
        });
      })
      .catch((error) => {
        console.log("Render failed");
        console.log(error);
      });
    });
  });
} else if (req.body.type === "FILESRC") {
  var imgToRender = req.body.imgSrc;
  var finishedImg = 'rendered' + i + '.jpg';
  fs.readFile("./public/images/" + imgToRender, function (err, imgdata ) {
    renderImage(imgdata).then((response) => {
      console.log("SUCCESS");
      var lines = response.data.split('\n');
      var imgStr = lines[lines.length - 2]; // Data we actually care about is in the second to last slot of the array
      var imgBuff =  Buffer.from(imgStr.substr(2).slice(0, -9), 'base64'); // Currently need to strip the extra b' and ending that Python adds
      fs.writeFile("./public/rendered/" + finishedImg, imgBuff, function (err) {
        if (err) {
          console.log("ERROR WRITING FILE");
          return next(err);
        }
        res.json({reqID: Number(req.body.reqID), origPath: imagesDir + imgToRender, startPath: imagesDir + imgToRender, renderedPath: "../rendered/" + finishedImg});
        i = i < 11 ? i + 1 : 0;
        res.end('Rendering finished');
      });
    })
    .catch((error) => {
      console.log("Render failed");
      console.log(error);
    });
  });
}
});

// Send an image to be rendered by the pix2pix function
function renderImage(imgdata) {
  return axios({
    method: 'post',
    url: 'http://10.54.98.51:31112/function/pix2pix-faas-base64',
    headers: {},
    data: imgdata
  });
}

const PORT = process.env.PORT || 8000;
const serverAddress = ip.address();
var server = app.listen(PORT, () => {
    console.log("Pix to Pix demo running..");
    console.log("Server listening: " + serverAddress + ` on port ${PORT}...`);
});

module.exports = app;
