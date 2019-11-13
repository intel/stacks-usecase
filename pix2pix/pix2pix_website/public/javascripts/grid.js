'use strict';
import {LitElement, html, css} from './lit-element.min.js';

class ItemGrid extends LitElement {

    static get properties() {
      return {
        numVisItem: { type: Number },
        itemsPerRow: { type: Number },
        imgArr: { type: Array },
        color: { type: String }
      };
    }

    static get styles() {
      return css`

      #grid {
        max-height: 100%;
        max-width: 100%;
        border-radius: 18px;
        color: #757575;
        display: flex;
        flex-wrap: wrap;
        align-content: flex-start;
        justify-content: center;
        align-items: center;
        overflow-y: auto;
      }

      .imgItem {
        max-width: 20%;
        max-height: 20%;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 5px;
      }
    `;
    }

    constructor() {
      super();

      // Get the pre-made images from the public/images folder
      fetch('/getImgJSON', {
        method: 'POST',
        body: "",
        headers: {
          'content-type': 'application/json'
        }
      }).then (function(res){
        return res.json();
      }.bind(this)).then(function(json){
        // Take the JSON reply and populate the image array.
        this.imgArr = [];
        for (let i = 0; i < json.children.length; i++) {
          this.imgArr[i] = {imgSrc: "../images/" + json.children[i].name, filename: json.children[i].name};
        }
      }.bind(this));

      this.imgArr = [];
    }

    render() {
      return html`
      <div id="grid">
          ${this.imgArr.map(i => html`<image class="imgItem" src=${i.imgSrc} data-filename=${i.filename} draggable="false"></image>`)}
      </div>
      `;
    }
  }

  customElements.define('item-grid', ItemGrid);