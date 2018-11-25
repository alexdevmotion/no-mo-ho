/*
 #noho-paraphraser {
 font-family: Raleway Semibold !important;
 }
 */

const css = `

#noho-paraphraser .noho-options {
  color: #4267b2;
  display: flex;
  flex-direction: column;
}

#noho-paraphraser .noho-options > div:hover {
  color: #6aa9ff;
  cursor: pointer;
}

#noho-paraphraser .ok-with-it {
  background: #4267b2;
  align-self: flex-end;
  padding: 5px;
  color: white;
  border-radius: 2%;
  cursor: pointer;
}

#noho-paraphraser .ok-with-it:hover {
background-color: #365899;
    border-color: #365899
}

#noho-paraphraser .bold-text {
  font-weight: bold;
  color: #e96a6a;
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
