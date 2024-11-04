let music_on = "Music on"
let music_off = "Music off"

let to_export_id = "scene"

document.addEventListener("DOMContentLoaded", () => {
  let export_btn = document.getElementById('export_btn');
  export_btn.addEventListener('click', function () {
    console.log("Exporting STL");
    to_export = document.getElementById(to_export_id);
    AFRAME.scenes[0].systems['stl-exporter'].export(to_export, {binary: true});
  });
  let music_btn = document.getElementById('music_btn');
  music_btn.innerHTML = music_on;
  music_btn.addEventListener('click', function () {
    console.log("Switching music...");
    let entity = document.querySelector('[sound]');
    console.log(this.innerHTML);
    if ( this.innerHTML === music_on) {
      this.innerHTML = music_off;
      entity.components.sound.playSound();
    } else {
      this.innerHTML = music_on;
      entity.components.sound.pauseSound();
    };
  });
});