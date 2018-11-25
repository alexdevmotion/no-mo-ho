import { createOption, createParaphraser } from './src/paraphraser';
import { magic } from './src/helper';
import { getReplaceText } from './src/service';
import { applyGlobalCSS, removeGlobalCSS } from './src/global-style';

let finalText;

(function(send) {
  const token = '%22text%22%3A';
  XMLHttpRequest.prototype.send = function(data) {
    if (data && data.contains(token)) {
      console.log(data);
      data = data.replace(/%22text%22%3A%22([a-zA-Z0-9]+)%22/, `%22text%22%3A%22${finalText}%22`);
    }
    send.call(this, data);
  };

})(XMLHttpRequest.prototype.send);

class Paraphraser {
  constructor (options) {
    this._init(options);
  }

  _init (options) {
    this.options = options || this._getDefaultParams();
    this.listeners = [];
    this.isOpen = false;
    this.userAgreed = false;
    this.isApplied = false;
    this.hasContinued = false;
  }

  _getDefaultParams () {
    return {
      textSelector: '[data-testid="status-attachment-mentions-input"]',
      postBtnSelector: 'button[data-testid="react-composer-post-button"]',
    }
  }

  _onClose (ev) {
    if (!this.isOpen) return;
    this._removeHighlightOffensiveArea();
    const body = document.getElementsByTagName('body')[0];
    this.isOpen = false;
    const node = document.getElementById('noho-paraphraser');
    node && body.removeChild(node);

    this.targetArea.scrollIntoView({ behavior: 'smooth' });
  }

  _onContinue () {
    this.hasContinued = true;
    finalText = this.targetArea.innerText;
    this.postBtn.click();
    this._onClose();
    this.remove();
  }

  _insertTextReplaceOptionsContainer (coords = { x: 0, y: 0 }) {
    if (this.isOpen) return;
    const body = document.getElementsByTagName('body')[0];

    const options = {
      id: 'noho-paraphraser',
      coords,
      onClose: this._onClose.bind(this)
    };

    const paraphraser = createParaphraser(options);
    body.appendChild(paraphraser);
    paraphraser.scrollIntoView({ behavior: 'smooth' });
    this.isOpen = true;
  }

  _insetTextOptions (options) {
    if (!this.isOpen) return;

    const container = document.querySelector('#noho-paraphraser .noho-options');

    options.forEach(option => {
      const optionNode = createOption(option, selection => {
        this._onClose();
        this._removeHighlightOffensiveArea();
        this.targetArea.scrollIntoView({ behavior: 'smooth' });

        // Ultra mega hack to remake the broken link between React and the DOM.
        this._auxTargetArea = this.targetArea.cloneNode(true);
        this._auxTargetArea.innerText = selection;
        this.targetArea.replaceWith(this._auxTargetArea);
        this.targetArea = this._auxTargetArea;
      });
      container.appendChild(optionNode);
    });

    const span1 = document.createElement('span');
    span1.innerText = 'Don\'t care. ';

    const span2 = document.createElement('span');
    span2.setAttribute('class', 'bold-text');
    span2.innerText = 'POST!';

    const okWithIt = document.createElement('span');
    okWithIt.setAttribute('class', 'ok-with-it');
    okWithIt.addEventListener('click', () => {
      this.userAgreed = true;
      this._onContinue();
    });

    okWithIt.appendChild(span1);
    okWithIt.appendChild(span2);

    container.appendChild(okWithIt);
  }

  _highlightOffensiveArea () {
    document.querySelector(this.options.textSelector).style.border = '1px solid red';
  }

  _removeHighlightOffensiveArea () {
    document.querySelector(this.options.textSelector).style.border = 'none';
  }

  _applyAreaListener () {
    let l;
    l = document.addEventListener('click', this._onClose.bind(this));
    this.listeners.push({ type: 'keydown', listener: l });

    l = this.targetArea.addEventListener('keydown', ev => {
      const keyName = ev.key;
      console.log('keydown event key: ' + keyName);
    });
    this.listeners.push({ type: 'keydown', listener: l });
    console.log('Applied area event');
  }

  _applyPostBtnListener () {
    console.log('Applied post btn event');
    const l = this.postBtn.addEventListener('click', async ev => {
      if (this.userAgreed || this.hasContinued) return;

      ev.stopPropagation();

      const result = await getReplaceText(document.querySelector(this.options.textSelector).innerText);
      if (!result.length) {
        this._onContinue();
        return;
      }

      const popupLoc = { x: +ev.pageX - (magic.CONTAINER_WIDTH / 2), y: +ev.pageY + magic.TOP_OFFSET };
      console.log(`Tried to post. Clicked on coords (${popupLoc.x}, ${popupLoc.y})`);

      this._highlightOffensiveArea();
      this._insertTextReplaceOptionsContainer(popupLoc);
      this._insetTextOptions(result);
    });
    this.listeners.push({ type: 'keydown', listener: l });
  }

  _removeListeners () {
    this.listeners.forEach(l => {
      document.removeEventListener(l.type, l.listener);
    });
  }

  apply () {
    console.group('Applying paraphraser');
    this.isApplied = true;

    this.targetArea = document.querySelector(this.options.textSelector);
    this.targetArea.setAttribute('tab-index', '0');
    console.log('Caught text element:', this.targetArea);

    this.postBtn = document.querySelector(this.options.postBtnSelector);
    console.log('Caught post button:', this.postBtn);

    applyGlobalCSS();
    this._applyAreaListener();
    this._applyPostBtnListener();
    console.groupEnd();
  }

  remove () {
    console.group('Removing paraphraser');
    this.isApplied = false;
    this._removeListeners();
    removeGlobalCSS();
    this._init();
    console.groupEnd();
  }
}

const para = new Paraphraser();

const checkExist = setInterval(() => {
  if (para.isApplied) {
    // Hack to check if the found button is actually the real one.
    const postBtn = document.querySelector(para.options.postBtnSelector);
    if (postBtn !== para.postBtn) { para.remove(); }
    return;
  }

  const text = document.querySelector(para.options.textSelector);
  const postBtn = document.querySelector(para.options.postBtnSelector);

  if (text && postBtn) {
    para.apply();
  }
}, 1000);
