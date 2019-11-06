import {LitElement, html, css} from './lit-element.min.js';

class HistoryBar extends LitElement {

    static get properties() {
      return {
        arrSize: { type: Number },
        numVisItem: { type: Number },
        itemsPerRow: { type: Number },
        resultArr: { type: Array },
        currIndex: { type: Number },
        color: { type: String },
      };
    }

    static get styles() {
      return css`

      #grid {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        overflow-y: auto;
      }

      result-item {
        margin-bottom: 4px;
        max-height: 100%;
        min-height: 30%;
        width: 97%;
      }
    `;
    }

    constructor() {
      super();
      this.itemsPerRow = 1;
      this.numVisItem = 1;
      this.currIndex = 0;
      this.resultArr = [];
    }

    render() {
      return html`
      <div id="grid">
          ${this.resultArr.map(i => html`<result-item id=${i.name} done=true startImg=${i.image} renderedImg=${i.rendPath}></result-item>`)}
      </div>
      `;
    }

    getColor(i) {
        var change = 100 / this.resultArr.length;
        var color = 255 - (i * change);
        return 'background-color: rgb(' + color + ',' + color + ',' + color +')';
    }

    // Add an item to the history array
    setItem(path, rendPath) {
      this.resultArr[this.currIndex] = {'name': this.currIndex, 'image': path, 'rendPath': rendPath};
      this.currIndex++;
      this.requestUpdate();
    }
  }

  customElements.define('result-bar', HistoryBar);
