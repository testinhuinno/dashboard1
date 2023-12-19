
const skinToggler = document.getElementById('skinToggler');

const toggleSkin = () => {
document.body.classList.toggle('dark');
}

document.querySelector("#theme-switcher").onchange = function() {
  var self = this;
  document.querySelectorAll("*").forEach(function(elem) {
    if(self.checked && elem.className.indexOf("light") !== -1) {
      elem.className = elem.className.replace("light", "dark");
    }else if(!self.checked && elem.className.indexOf("dark") !== -1) {
      elem.className = elem.className.replace("dark", "light");
    }
  });
}