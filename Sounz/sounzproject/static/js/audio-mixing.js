const audioContext = new (window.AudioContext || window.webkitAudioContext)();
let baseAudioUrlOne = document.getElementById('base-audio-storage').value;  // Base audio URL
let collabIdOne = document.getElementById('collabId').value;
function getCSRFToken() {
    return document.getElementById("csrf-token").value;
}

// Fetch audio URLs from backend
async function fetchAudioFiles() {
    try {
        const response = await fetch(`/get-audio-files?collabId=${collabIdOne}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data.audio_urls; // Expecting an array of URLs
    } catch (error) {
        console.error("Error fetching audio files:", error);
        return [];
    }
}

// Load and decode audio files from URLs
async function loadAndDecodeAudio(urls) {
    const buffers = [];
    for (const url of urls) {
        try {
            const response = await fetch(url);
            const arrayBuffer = await response.arrayBuffer();
            const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
            buffers.push(audioBuffer);
        } catch (error) {
            console.error(`Error loading audio file ${url}:`, error);
        }
    }
    return buffers;
}

// Mix the audio buffers and convert to MP3
async function mixMultipleAudioFiles() {
    const userAudioURLs = await fetchAudioFiles();
    const allAudioURLs = [baseAudioUrlOne, ...userAudioURLs];  

    if (allAudioURLs.length < 2) {
        alert('Not enough audio files available for mixing.');
        return;
    }

    const buffers = await loadAndDecodeAudio(allAudioURLs);
    if (buffers.length < 2) {
        console.error("Failed to decode enough audio files.");
        return;
    }

    const maxDuration = Math.max(...buffers.map(buffer => buffer.duration));
    const mixedBuffer = audioContext.createBuffer(
        2, 
        audioContext.sampleRate * maxDuration, 
        audioContext.sampleRate
    );

    // Mixing audio
    buffers.forEach(buffer => {
        for (let channel = 0; channel < mixedBuffer.numberOfChannels; channel++) {
            const mixedChannelData = mixedBuffer.getChannelData(channel);
            const bufferChannelData = buffer.getChannelData(channel % buffer.numberOfChannels);
            const bufferLength = bufferChannelData.length;

            for (let i = 0; i < bufferLength && i < mixedChannelData.length; i++) {
                mixedChannelData[i] += bufferChannelData[i];
            }
        }
    });

    // Normalize mixed audio
    for (let channel = 0; channel < mixedBuffer.numberOfChannels; channel++) {
        const mixedChannelData = mixedBuffer.getChannelData(channel);
        let maxAmplitude = 0;

        for (let i = 0; i < mixedChannelData.length; i++) {
            maxAmplitude = Math.max(maxAmplitude, Math.abs(mixedChannelData[i]));
        }

        if (maxAmplitude > 1) {
            for (let i = 0; i < mixedChannelData.length; i++) {
                mixedChannelData[i] /= maxAmplitude;
            }
        }
    }

    // Convert to MP3
    const audioBlob = await convertToMP3(mixedBuffer);

    //  Upload to Django
    uploadMixedAudio(audioBlob);
}

// Convert AudioBuffer to MP3
async function convertToMP3(audioBuffer) {
    const offlineContext = new OfflineAudioContext(
        audioBuffer.numberOfChannels,
        audioBuffer.length,
        audioBuffer.sampleRate
    );

    const source = offlineContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(offlineContext.destination);
    source.start();

    const renderedBuffer = await offlineContext.startRendering();
    const pcmData = renderedBuffer.getChannelData(0);

    return encodeMP3(pcmData, audioBuffer.sampleRate);
}

// Encode PCM to MP3
function encodeMP3(pcmData, sampleRate) {
    const mp3Encoder = new lamejs.Mp3Encoder(1, sampleRate, 128); 
    const samples = new Int16Array(pcmData.length);

    for (let i = 0; i < pcmData.length; i++) {
        samples[i] = pcmData[i] * 32767;
    }

    const mp3Data = mp3Encoder.encodeBuffer(samples);
    return new Blob([new Uint8Array(mp3Data)], { type: "audio/mp3" });
}

//  Upload the mixed MP3 to Django
async function uploadMixedAudio(audioBlob) {
    const file = new File([audioBlob], `mixed_audio_${Date.now()}.mp3`, { type: "audio/mpeg" });

    const formData = new FormData();
    formData.append("mixed_audio", file);
    formData.append("collaboration_id", collabIdOne);  
    console.log(file);
    console.log(collabIdOne);
    try {
        console.log("test1");
        const response = await fetch("upload-mixed-audio/", {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": getCSRFToken() }
        })
        .then(response => response.json())
        .then(data => {
            if (data.redirect) {
            window.location.href = data.redirect;
        }
        })
        console.log("test2");
        const result = await response.json();
        console.log("Upload successful:", result);
    } catch (error) {
        console.error("Upload failed:", error);
    }
}

// Button event listener
document.getElementById('collab-confirmed').addEventListener('click', mixMultipleAudioFiles);

function showPopUp() {
    var popup = document.getElementById("popup");
    popup.classList.toggle("show");
}
function showEndpopup() {
    var popup = document.getElementById("popup-end");
    popup.classList.toggle("show");
}

function toggleDropdown(event) {
    event.stopPropagation();
    let dropdown = document.getElementById("dropdownMenu");

    if (dropdown.style.display === "block") {
        dropdown.style.display = "none";
    } else {
        dropdown.style.display = "block";

        // Position dropdown near the button
        let rect = event.target.getBoundingClientRect();
        dropdown.style.top = 707 + "px";
        dropdown.style.right = 10 + "px";
    }
}
document.addEventListener("click", function () {
    document.getElementById("dropdownMenu").style.display = "none";
});
function end_collab() {
    console.log(`Deleting audio with Sync ID: ${collabIdOne}`);
    fetch(`/end-collab?collabId=${collabIdOne}`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())  // Parse JSON response
    .then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url;  // Redirect manually
        }
    })
    .catch(error => console.error("Error:", error));
}
function showEditpopup(){
    var popup = document.getElementById("popup-edit");
    popup.classList.toggle("show");
}
function save_finalpost() {
    let formData = new FormData(document.getElementById("register-form"));
    formData.append("collabId", collabIdOne);

    fetch("/update-collab-post/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Collaboration details updated successfully!");
            location.reload();
        } else {
            console.log("Failed to update collaboration details.");
        }
    })
    .catch(error => console.error("Error:", error));
}
