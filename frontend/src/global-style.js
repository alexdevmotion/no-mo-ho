const css = `
#noho-paraphraser .noho-options > div:hover {
  color: #4267b2;
  cursor: pointer;
}
`;
const head = document.getElementsByTagName('head')[0];

let style;
export function applyGlobalCSS () {
  style = document.createElement('style');
  style.type = 'text/css';

  if (style.styleSheet) {
    style.styleSheet.style = css;
  } else {
    style.appendChild(document.createTextNode(css));
  }

  head.appendChild(style);
}

export function removeGlobalCSS () {
  head.removeChild(style);
}
