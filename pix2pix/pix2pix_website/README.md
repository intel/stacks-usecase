# Pix 2 Pix demo

A demonstration of Deep Learning and FaaS
# Prerequisites
- node
- npm
- Google Chrome
- An OpenFaas deployment that has a pix2pix function

# Installation
From the pix2pix_website directory, install the required npm packages.
```
npm install
```
# Usage
## To start the demo the easy way
This will start the nodejs app and launch a browser running the webapp in fullscreen mode.
```
npm run demo
```
## To start serving the demo manually
**To start the node.js server**

```
node app.js
```

**To connect the webapp**


Open a browser and go to localhost:8000

# To add example images
If you want to add more example images, just copy them to public/images and the server will pick them up and supply them to the client. Note that any new images added won't be seen until the server is restarted.

# How it all works
## The parts:
## **Node.js server**
- **app.js** is run by node.js in the background, it hosts the webapp and holds all the pre and post rendered images. It also serves as a communication layer between the webapp and the FaaS server.
## **Webapp (demo):**
Written using lit-element to create encapsulated web elements. Each javascript file contains a single element, whose CSS and other attributes will not interfere with other elements. Elements communicate using custom events
- **pix-demo-app.js** is the main file for the webapp.
- **draw.js** is the code for the 'Draw your own' page of the webapp.
- **colorselect.js** is the code for the color select bar in the draw page.
- **grid.js** is the code for the 'Image Select' page of the webapp.
- **history.js** is the code for the 'History' page of the webapp.
- **result.js** is the code for the result element. This is used as the main result on the page and for all the items in the history.

## **The flow:**
- Upon clicking 'Render' on the Draw page or selecting an image on the Image Select page, the webapp will bring up a pending result element. The result will show the starting image and a 'Working' animation while it waits for the result from the server.
- A POST '/render' call is made, which app.js will handle. For the Draw page an image buffer from the canvas element is sent, for the Image Select page a image URL is sent.
- app.js will then call the function **app.post('/render'...**, which will use the provided REST API to send an image to the FaaS server for rendering.
- FaaS server will return the rendered image, and app.js will then finish the reply to the POST '/render' call. This reply will contain the request ID, the starting image path, and the rendered image path.
- The webapp will get the reply and will disply the result on the main page and add the result to the history. Note that only 12 items are stored in the history, and will be overwritten as the demo is run more than 12 times. This number is arbitrary and can be increased or decreased if desired.