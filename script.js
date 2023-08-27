const DISPLAY = document.querySelector('#display');
const INFO = document.querySelector('#info');
const PLAYED = document.querySelector('#played');
const KEYBOARD = document.querySelector('#keyboard');

const LOAD = document.querySelector('#load');
const SAVE = document.querySelector('#save');
const LOAD_LABEL = document.querySelector("#loadLabel");

const DEFAULT_FILE_NAME = 'my-midi';
const CLASS = 'keyboard__note--pressed';
const NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
const KEYMAP = ['a', 'w', 's', 'e', 'd', 'f', 't', 'g', 'y', 'h', 'u', 'j', 'k', 'o', 'l', 'p'];
const SYNTH = new Tone.Synth().toDestination();
const NOW = Tone.now();

myPianoRollVisualizer
const MIDIVis = document.getElementById("#myPianoRollVisualizer");
// Allow to store the current note in an index, for duration computation
const CURRENT = {};
const RECORDED = [];

let isRecording = false;
let isLoop = false;
let recordingTime = 0;
let theLoop;
let octave = 4;
let output;




// Listen external Midi IO
const listenWebMidi = () => {
  WebMidi.enable(function (err) {
    // Get the first real device
    input = WebMidi.inputs.filter(input => !!input.manufacturer)[0];
    output = WebMidi.outputs.filter(output => !!output.manufacturer)[0];
    
    

    if (input) {
      const { version, manufacturer, name } = input;
      INFO.innerText = [version, manufacturer, name].join(' - ');

      // TODO: Create a map to retrieve length of playing time
      input.addListener('noteon', 'all', (event) => {
        const [something, note, volume] = event.data;
        play(note, volume)
      })
      input.addListener('noteoff', 'all', (event) => {
        const [something, note, volume] = event.data;
        play(note, 0)
      }) 
    }
  })
} 

// Initialize keyboard to play from PC
const listenKeyboard = () => {
  // TODO: Verify why 8 and somewhere else 4
  const offset = 8;
  
  document.addEventListener('keydown', event => {
    const {key, repeat} = event;
    const pos = KEYMAP.indexOf(key);
    if (pos >= 0 && !repeat) {
      const note = pos + offset + octave * 8;
      play(note);
    }
  })

  // TODO: Create a map to retrieve length of playing time
  document.addEventListener('keyup', event => {
    const key = event.key;
    const pos = KEYMAP.indexOf(key);
    
    if (pos >= 0) {
      const note = pos + offset + octave * 8;
      play(note, 0);
    }
  });
}

const load = () => {
  const file = LOAD.files[0];
  if (!file) return;

  LOAD_LABEL.textContent = file.name;

  const reader = new FileReader();
  reader.onload = (e) => {
    const midi = new Midi(e.target.result);
    // TODO: Replace when allow multiple loops
    const piano = midi.tracks
      .filter(track => ['piano', 'guitar'].includes(track.instrument.family))
      .filter(track => track.notes.length)[0];
    // TODO: Replace after refactorying note object to match tone.js
    const notes = piano.notes.map(n => {
      return {
        note: n.midi,
        volume: n.velocity * 100,
        time: n.ticks,
        duration: n.duration
      }
    })

    RECORDED.length = 0;
    RECORDED.push(...notes);
    console.log(JSON.stringify(notes))
    PLAYED.innerText = RECORDED
      .filter(note => !!note.volume)
      .map(note => inputToNote(note.note))
      .join(', ');
  };
  reader.readAsArrayBuffer(file);
};

// Listen input file for midi loading
const listenLoad = () => {
  LOAD.onchange = load;
}

const save = () => {
  const midi = new Midi()
  const track = midi.addTrack()
  RECORDED.forEach(
    note => track.addNote({
      midi: note.note,
      time: note.time / 1000,
      duration: note.time || 0.2,
      velocity: note.volume
    })
  )


  const saveAs = prompt('Save midi file as:', DEFAULT_FILE_NAME);
  const fileName = `${saveAs || DEFAULT_FILE_NAME}.mid`;
  const data = midi.toArray();
  const blob = new Blob([data], {type: 'audio/midi audio/x-midi'});

  const elem = window.document.createElement('a');
  elem.href = window.URL.createObjectURL(blob);
  elem.download = fileName;        
  document.body.appendChild(elem);
  elem.click();        
  document.body.removeChild(elem);
}

const listenSave = () => {
  SAVE.onclick = save;
}

// Reset everything
const reset = () => {
  RECORDED.length = 0;
  PLAYED.innerText = '';
  DISPLAY.innerText = '';
  isRecording = false;
  isLoop = false;
}

// Map Inpput value to actual note
const inputToNote = (input) => {
  // TODO: Verify why 4
  const offset = 4;
  const inputOffset = input - offset;
  const size = NOTES.length;
  const octave = Math.floor(inputOffset/size);
  const pos = inputOffset - size * octave;
  const note = `${NOTES[pos]}${octave}`;
  
  return note;
}

const play = (note, volume = 50, duration) => {

  const key = document.querySelector(`#key${note}`);
  const tone = inputToNote(note);
  DISPLAY.innerText = note + ' - ' + tone;
  console.log(PLAYED)
  
  const remove = () => {
    key?.classList?.remove(CLASS);
    SYNTH.triggerRelease(Tone.now() + '8n')
    if (output) {
      output.stopNote(tone);
    }
  }
  
  if (!!volume) {
    SYNTH.triggerAttack(tone, Tone.now())
    key?.classList?.add(CLASS);
    
    if (output) {
      output.playNote(tone);
    }
    
    if (duration) {
      setTimeout(() => remove(), duration * 1000);
    }
  } else  {
    remove();
  }
  
  if(isRecording) {
    const time = Math.floor(performance.now() - recordingTime);
    RECORDED.push({note, volume, time, duration})
    PLAYED.innerText = RECORDED
      .filter(note => !!note.volume)
      .map(note => inputToNote(note.note))
      .join(', ');
  }
}

// Start recording
const record = (status) => {
  isRecording = status;
  recordingTime = performance.now();
};

// Start loop
const loop = () => {
  isLoop = !isLoop;
  isRecording = false;
  if(RECORDED.length) {
    const loopLength = RECORDED[RECORDED.length -1].time;

    if (isLoop) {
      loopNotes();
      theLoop = setInterval(() => loopNotes(), loopLength);
    } else {
      clearInterval(theLoop)
    }
  }
};

const loopNotes = () => {
  RECORDED.forEach(note => {
    setTimeout(() => {
      // Prevent to keep playing also after stop
      if (!isLoop) return;
      
      play(note.note, note.volume, note.duration)
      // setTimeout(() => play(note.note, 0), 200)
    }, note.time);
  })
}

/*

const file = "generate.py"
async function runPythonFile(file, model) {
  await pyodide.load();
  
  const reader = new FileReader();
  reader.onload = async () => {
    const fileContent = reader.result;
    const pythonScript = new TextDecoder().decode(fileContent);
    const result = pyodide.runPython(pythonScript);
    console.log(result);
  };

  reader.readAsArrayBuffer(file);
}

function generateRock(model="models/rockmodel.pt"){
  runPythonFile(file, model);
}
function generateClassical(){
  function generateRock(model="models/classicalmodel.pt"){
    runPythonFile(file, model);
  }
}
function generatePop(){
  function generateRock(model="models/popmodel.pt"){
    runPythonFile(file, model);
  }
}
function generateMetal(){
  function generateRock(model="models/metalmodel.pt"){
    runPythonFile(file, model);
  }
}
function generateJazz(){
  function generateRock(model="models/jazzmodel.pt"){
    runPythonFile(file, model);
  }
}


*/


const close = () => {}

const add = () => {}

// listenMidi();
listenWebMidi();
listenKeyboard();
listenLoad();
listenSave();
