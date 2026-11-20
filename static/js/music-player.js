
(() => {
  "use strict";

  function initMusicPlayer() {
    const player = document.getElementById("sendevMusic");
    const audio = document.getElementById("sendevAudio");
    const toggle = document.getElementById("sendevMusicPlay");
    const compact = document.getElementById("sendevMusicCompact");
    const slider = document.getElementById("sendevMusicVolume");
    const output = document.getElementById("sendevVolumeValue");
    const status = document.getElementById("sendevMusicStatus");

    if (!player || !audio || !toggle ||
        !compact || !slider || !output || !status) {
      console.error(
        "SenDev Radio: Elemen HTML pemutar musik tidak lengkap."
      );
      return;
    }

    let startVolume = 25;

    try {
      const stored = localStorage.getItem("sendev_music_volume");
      if (stored !== null) {
        const value = Number(stored);
        if (Number.isFinite(value)) {
          startVolume = Math.max(0, Math.min(100, value));
        }
      }
    } catch (error) {
      console.warn("Penyimpanan volume tidak tersedia.");
    }

    audio.volume = startVolume / 100;
    slider.value = String(startVolume);
    output.value = `${startVolume}%`;

    function render() {
      const playing = !audio.paused && !audio.ended;

      player.classList.toggle("is-playing", playing);
      toggle.setAttribute("aria-pressed", String(playing));
      toggle.setAttribute(
        "aria-label",
        playing ? "Jeda musik" : "Putar musik"
      );

      if (playing) {
        status.dataset.error = "false";
        status.textContent = "Sedang diputar • SenDev Radio";
      } else if (status.dataset.error !== "true") {
        status.textContent = "Dijeda • klik Play";
      }
    }

    toggle.addEventListener("click", async () => {
      if (!audio.paused) {
        audio.pause();
        return;
      }

      status.dataset.error = "false";
      status.textContent = "Memuat lagu...";

      try {
        await audio.play();
        render();
      } catch (error) {
        console.error("SenDev Radio gagal memutar:", error);

        status.dataset.error = "true";

        if (error.name === "NotAllowedError") {
          status.textContent = "Pemutaran diblokir browser";
        } else if (error.name === "NotSupportedError") {
          status.textContent = "Format audio tidak didukung";
        } else {
          status.textContent = "Gagal memuat lagu";
        }

        render();
      }
    });

    slider.addEventListener("input", () => {
      const value = Math.max(
        0,
        Math.min(100, Number(slider.value) || 0)
      );

      audio.volume = value / 100;
      output.value = `${value}%`;

      try {
        localStorage.setItem(
          "sendev_music_volume",
          String(value)
        );
      } catch (error) {
        console.warn("Volume tidak dapat disimpan.");
      }
    });

    compact.addEventListener("click", () => {
      const minimized = player.classList.toggle("is-compact");

      compact.setAttribute(
        "aria-expanded",
        String(!minimized)
      );
      compact.setAttribute(
        "aria-label",
        minimized
          ? "Perluas pemutar musik"
          : "Minimalkan pemutar musik"
      );
    });

    audio.addEventListener("play", render);
    audio.addEventListener("pause", render);
    audio.addEventListener("ended", render);

    audio.addEventListener("error", () => {
      status.dataset.error = "true";
      status.textContent = "File lagu gagal dimuat";

      console.error(
        "SenDev Radio: Periksa file MP3:",
        audio.currentSrc || audio.querySelector("source")?.src
      );

      render();
    });

    render();
    console.log("SenDev Radio berhasil diinisialisasi.");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initMusicPlayer);
  } else {
    initMusicPlayer();
  }
})();
