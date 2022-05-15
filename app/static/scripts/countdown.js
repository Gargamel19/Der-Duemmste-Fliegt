
    function idset(id, string) {
  document.getElementById(id).innerHTML = string;
}

function countdown_start_stop() {
const btn = document.getElementById("countdown_start_stop")
  if (btn.classList.contains("unloaded")) {
        btn.classList.remove("unloaded")
        btn.classList.add("started")
        btn.textContent = "Stop";
        countdown.start();
    } else if (btn.classList.contains("started")) {
        btn.classList.remove("started")
        btn.classList.add("stopped")
        btn.textContent = "Start";
        countdown.stop();
    } else if (btn.classList.contains("stopped")) {
        btn.classList.remove("stopped")
        btn.classList.add("started")
        btn.textContent = "Stop";
        countdown.resume();
    }
}

var countdown = (function() {
  var stop = 1;
  var mins = 0;
  var secs = 0;
  var msecs = 0;
  var runden = "";
  var anzrunden = 0;
  return {
    start: function() {
      mins = document.getElementById("countdown_min").value;
      secs = document.getElementById("countdown_sec").value;
      stop = 0;
    },
    resume: function() {
      stop = 0;
    },
    stop: function() {
      stop = 1;
    },
    clear: function() {
      countdown.stop();
      mins = document.getElementById("countdown_min").value;
      secs = document.getElementById("countdown_sec").value;
      msecs = 0;
      runden = "";
      anzrunden = 0;
      countdown.html();
    },
    restart: function() {
      countdown.clear();
      countdown.start();
    },



    timer: function() {
      if (stop === 0) {
        msecs--;
        if (msecs === -1) {
          secs --;
          msecs = 99;
        }
        if (secs === -1) {
          mins--;
          secs = 59;
        }
        countdown.html();
      }
    },
    runde: function() {
      runden = "</td><td>" + mins + "</td><td>" + secs + "</td><td>" + msecs + "</td></tr>" + runden;
      anzrunden++;
      countdown.html();
    },
    set: function(minuten, sekunden, msekunden) {
      countdown.stop();
      mins = minuten;
      secs = sekunden;
      msecs = msekunden;
      runden = "";
      anzrunden = 0;
      countdown.html();
    },
    html: function() {
      idset("countdown_minuten", ("00" + mins).slice(-2));
      idset("countdown_sekunden", ("00" + secs).slice(-2));
      idset("countdown_msekunden", ("00" + msecs).slice(-2));
      idset("countdown_runden", runden);
      idset("countdown_anzrunden", anzrunden + " Runden");
    }
  }
})();
setInterval(countdown.timer, 10);