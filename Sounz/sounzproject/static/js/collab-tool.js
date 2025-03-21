function getCSRFToken() {
    return document.cookie.split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}

let baseAudioUrl = document.getElementById('base-audio-storage').value;
let collabId = document.getElementById('collabId').value;
let userId = document.getElementById('userId').value;
let waveSurfers = {};
let isRecording = false;
let mediaRecorder;
let audioChunks = [];
let micStream = null;
let audioFile;
let audioURL;
let UploadAudioURL;
let audioBlob;
let UploadBlob;
let control_flag = 'ready';

initWaveSurfer("base-audio-graph",baseAudioUrl, 'rgb(219, 175, 255)');
updateApprovalStatus();
const recordButton = document.getElementById("masterPlayRecord");
const stopRecordingButton = document.getElementById("masterStopRecord");
const pauseRecordingButton = document.getElementById("pauseRecording");
const playAllButton = document.getElementById("masterPlay");
const pauseAllButton = document.getElementById("masterPause");
const stopAllButton = document.getElementById("masterStop");
const gRSync = document.getElementById("g-rSync-container");
const gSyncButton = document.getElementById('g-rSync-sync');    
const gRedoButton = document.getElementById('g-rSync-redo');    
const gSyncContainer = document.getElementById('main-sync-container');    
const refreshButton = document.getElementById('refresh');    
const g_rSyncContainer = "g-rSync-audio-graph";    
const deleteaudio = document.getElementById('audio-delete');
const audioUpload = document.getElementById('audioUpload');
const masterVolume = document.getElementById('master-volume');
const recordBar = document.getElementById('bars-recording');
const uploadButton = document.getElementById('uploadLabel');
const resumeRec = document.getElementById('resume-rec');


function initWaveSurfer(containerId, audioFile, color) {
    let waveSurfer = WaveSurfer.create({
        container: `#${containerId}`,
        waveColor: color,
        progressColor: 'rgb(0, 115, 255)',
        // cursorColor: '#d9d9d9',
        dragToSeek: true,
        height: 100,
        barWidth: 1,
        barRadius: 3,
        barGap: 1,
        partialRender: true,
        responsive: true,
        normalize: true, 
        barHeight: 1,  
        amplitude: 0.5,
        fillParent: true,
        minPxPerSec: 0,
        autoScroll: false,
        backend: 'WebAudio',
        url: audioFile,
    });

    waveSurfers[containerId] = waveSurfer;

    return waveSurfer;
} 
document.addEventListener("click", function(event) {
    if (event.target.classList.contains("single-audio-play")) {
        let containerId = event.target.getAttribute("data-container");
        if (waveSurfers[containerId]) waveSurfers[containerId].play();
    }

    if (event.target.classList.contains("single-audio-pause")) {
        let containerId = event.target.getAttribute("data-container");
        if (waveSurfers[containerId]) waveSurfers[containerId].pause();
    }

    if (event.target.classList.contains("single-audio-stop")) {
        let containerId = event.target.getAttribute("data-container");
        if (waveSurfers[containerId]) waveSurfers[containerId].stop();
    }
});

document.addEventListener("input", function(event) {
    if (event.target.classList.contains("single-volume")) {
        let containerId = event.target.getAttribute("data-container");
        if (waveSurfers[containerId]) {
            waveSurfers[containerId].setVolume(event.target.value);
        }
    } 
});
if (masterVolume) {
    masterVolume.addEventListener("input", function() {
        let volumeValue = masterVolume.value;
        Object.values(waveSurfers).forEach(ws => ws.setVolume(volumeValue));
        document.querySelectorAll(".single-volume").forEach(slider => {
            slider.value = volumeValue;
        });
    });
}
async function isHeadphonePlugged() {
    try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        return devices.some(device => device.kind === "audiooutput" && device.label.toLowerCase().includes("headphone"));
    } catch (error) {
        console.error("Error detecting headphones:", error);
        return false;
    }
}
recordButton.addEventListener("click", async () => {
    control_flag = 'rec';
    if (!isRecording) {
        try {
            const headphonePlugged = await isHeadphonePlugged();

            micStream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: !headphonePlugged,
                    noiseSuppression: !headphonePlugged,
                    autoGainControl: !headphonePlugged,
                    channelCount: 2
                }
            });

            mediaRecorder = new MediaRecorder(micStream, { mimeType: "audio/webm;codecs=opus" });
            audioChunks = [];

            mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);

            mediaRecorder.onstop = () => {
                micStream.getTracks().forEach(track => track.stop());
                micStream = null;

                audioBlob = new Blob(audioChunks, { type: "audio/webm" });
                audioURL =URL.createObjectURL(audioBlob)
                initWaveSurfer("g-rSync-audio-graph",audioURL);
                
                

                gRSync.style.display="block";
            };

            Object.values(waveSurfers).forEach(ws => ws.play());
            mediaRecorder.start();
            isRecording = true;

            pauseRecordingButton.disabled = false; 
            stopRecordingButton.disabled = false; 
            recordButton.style.display='none';
            recordBar.style.display='flex';
            uploadButton.disabled=true;

        } catch (err) {
            console.error("Microphone access denied or error occurred:", err);
        }
    }
});
stopRecordingButton.addEventListener("click", () => {
    if (isRecording) {
        mediaRecorder.stop();
        isRecording = false;

        Object.values(waveSurfers).forEach(ws => ws.stop());
        
        recordBar.style.display='none';
        recordButton.style.display='flex';
        recordButton.disabled=true;
        stopRecordingButton.disabled=true;
        pauseRecordingButton.disabled=true;
        pauseRecordingButton.style.display='flex';
    }
});
pauseRecordingButton.addEventListener("click", () => {
    if (mediaRecorder.state === "recording") {
        mediaRecorder.pause();
        pauseRecordingButton.style.display='none';
        resumeRec.style.display='flex';
        Object.values(waveSurfers).forEach(ws => ws.pause());
    } });
resumeRec.addEventListener("click", () => {
    if (mediaRecorder.state === "paused") {
        mediaRecorder.resume();
        pauseRecordingButton.style.display='flex';
        resumeRec.style.display='none';
        Object.values(waveSurfers).forEach(ws => ws.play());
    }
});
playAllButton.addEventListener("click", () =>{Object.values(waveSurfers).forEach(ws => ws.play())});
pauseAllButton.addEventListener("click", () =>{Object.values(waveSurfers).forEach(ws => ws.pause())});
stopAllButton.addEventListener("click", () =>{Object.values(waveSurfers).forEach(ws => ws.stop())});

async function blobToFile(blob, filenamePrefix) {
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.readAsArrayBuffer(blob);
        reader.onloadend = async () => {
            const audioContext = new AudioContext({ sampleRate: 44100 });
            const audioBuffer = await audioContext.decodeAudioData(reader.result);
            
            const offlineContext = new OfflineAudioContext({
                numberOfChannels: 1,
                length: audioBuffer.length,
                sampleRate: 44100
            });

            const source = offlineContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(offlineContext.destination);
            source.start();

            const renderedBuffer = await offlineContext.startRendering();
            const pcmData = renderedBuffer.getChannelData(0);

            // Convert Float32 to Int16
            const int16Array = new Int16Array(pcmData.length);
            for (let i = 0; i < pcmData.length; i++) {
                int16Array[i] = Math.max(-32768, Math.min(32767, pcmData[i] * 32768));
            }

            const mp3Encoder = new lamejs.Mp3Encoder(1, 44100, 192);
            const mp3Data = mp3Encoder.encodeBuffer(int16Array);
            const mp3Blob = new Blob([new Uint8Array(mp3Data)], { type: "audio/mpeg" });

            resolve(new File([mp3Blob], `${filenamePrefix}_${Date.now()}.mp3`, { type: "audio/mpeg" }));
        };
    });
}
gSyncButton.addEventListener("click", async() =>{
    if (control_flag == 'rec'){
        const uniqueFileName = `recorded_${crypto.randomUUID()}`;
        audioFile = await blobToFile(audioBlob, uniqueFileName);
    }
    else if (control_flag == 'upl'){
        const uniqueFileName = `uploaded_${crypto.randomUUID()}`;
        audioFile = await blobToFile(UploadBlob, uniqueFileName);
    }
    console.log(audioFile);
    const formData = new FormData();
    formData.append("syncMedia", audioFile);
    formData.append("collaboration_id", collabId);  
    try {
        const response = await fetch("/upload-sync-audio/", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        console.log("Upload success:", result);
        deleteWaveSurfer(g_rSyncContainer);
        gRSync.style.display="none";
        refreshContent();
    } catch (error) {
        console.log("Upload error:", error);
    }
});
refreshContent();
function refreshContent() {
    fetch(`workspace?collab-id=${collabId}`, { 
        headers: { "X-Requested-With": "XMLHttpRequest" }  
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.audio_list && data.audio_list.length > 0) {
            console.log(data.audio_list);
            gSyncContainer.innerHTML="";
            data.audio_list.forEach(audioDT => {
                const newElement = `
                    <div class="sync-audio-container main-each-container">
                        <div class="sync-audio-graph-${audioDT.syncId} b-s-Allaudio" data-value="${audioDT.syncId}" id="sync-audio-graph-${audioDT.syncId}"></div>
                        <div class="sync-audio-controls audio-control">
                            <div class="sync-audio-data">
                                <p id="audio-content" class="audio-contents-text">
                                    <span id="username" class="content">${audioDT.syncedBy__username}</span>
                                    <span id="divider" class="content">•</span>
                                    <span id="audio-name-${audioDT.syncId}" class="content">${audioDT.audioName || "Audio_XXX"}</span>
                                </p>
                            </div>
                            <div id="sync-audio-control-panel" class="controls">
                                <div class="control-sync pps-c">
                                    <img class="single-audio-play control-button-images" src="/static/images/audio-play.svg" data-container="sync-audio-graph-${audioDT.syncId}" alt="play-button">
                                    <img class="single-audio-pause control-button-images" src="/static/images/audio-pause.svg" data-container="sync-audio-graph-${audioDT.syncId}" alt="pause-button">
                                    <img class="single-audio-stop control-button-images" src="/static/images/audio-stop.svg" data-container="sync-audio-graph-${audioDT.syncId}" alt="stop-button">    
                                </div>
                                <div class="volume-sync volume">
                                    <label for="volume" class="volume-icon"><img class="single-volume-icon control-button-images" src="/static/images/audio-volume.svg" alt="volume-button"></label>
                                    <input type="range" data-container="sync-audio-graph-${audioDT.syncId}" class="single-volume" id="volume" min="0" max="1" step="0.01" value="1">
                                </div>
                                <div class="download-base" style="margin-left: 15px;">
                                    <a id="download-audio-${audioDT.syncId}" class="download-btn" href="/media/${audioDT.syncMedia}" download>
                                        <img class="control-button-images" src="/static/images/download-button.svg" alt="Download">
                                    </a>
                                </div>
                                <button class="audio-delete" id="audio-delete" data-container="sync-audio-graph-${audioDT.syncId}" onclick=deleteAudio("${audioDT.syncId}") data-value="${audioDT.syncId}"><img class="single-audio-delete control-button-images" src="/static/images/audio-delete.svg" alt="delete-button"></button>
                            </div>
                        </div>
                    </div>
                `;

                gSyncContainer.insertAdjacentHTML("beforeend", newElement);
                
                initWaveSurfer(`sync-audio-graph-${audioDT.syncId}`,`/media/${audioDT.syncMedia}`, 'rgb(142, 206, 255)');
            });
        }
        else{
            // Object.keys(waveSurfers).forEach(key => {
            //     if(waveSurfer[key]=="base-audio-graph"){continue;}
            //     waveSurfers[key].destroy();
            //     delete waveSurfers[key];
            // });
            gSyncContainer.innerHTML="";
        }
    })
    
    .catch(error => console.error("Error:", error));
};
refreshButton.addEventListener("click", () =>{
    refreshContent();
});
function deleteWaveSurfer(cntr) {
    if (waveSurfers[cntr]) {
        waveSurfers[cntr].destroy();
        delete waveSurfers[cntr]; 
    }
}
gRedoButton.addEventListener("click",() =>
    {
        deleteWaveSurfer(g_rSyncContainer);
        gRSync.style.display="none";
    });

function deleteAudio(syncId) {
    console.log(`Deleting audio with Sync ID: ${syncId}`);
    fetch(`/delete-audio?syncId=${syncId}`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "X-Requested-With": "XMLHttpRequest"
        }
    });
    console.log("deleted");
    refreshContent();
    const theContainer = "sync-audio-graph-"+syncId;
    console.log(theContainer);
    deleteWaveSurfer(theContainer);
}
function approveButton(button, status) {
    fetch(`/approval-update?cId=${collabId}&status=${status}&userId=${userId}`, {
        method: "PATCH",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            buttonA = document.getElementById('approval-button');
            // Toggle button text and status
            if (status === "approve") {
                buttonA.textContent = "Revoke";
                buttonA.setAttribute("onclick", "approveButton(this, 'revoke')");
            } else {
                buttonA.textContent = "Approve";
                buttonA.setAttribute("onclick", "approveButton(this, 'approve')");
            }

            // Update approval count dynamically
            updateApprovalStatus();
        }
    })
    .catch(error => console.error("Error:", error));
}
function updateApprovalStatus() {
    fetch(`/get-approval-status?cId=${collabId}`)
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            document.getElementById("popup-collab-terminated").style.display = "flex";
            
            setTimeout(() => {
                document.getElementById("popup-collab-terminated").style.display = "none";
                window.location.href = data.redirect; 
            }, 3000);
        }
        document.getElementById("accept-count").innerText = data.accept_count;
        if (data.accept_count >= data.owner_count) {
            document.getElementById("upload-warning-button").style.display = "block";
            document.getElementById("upload-warning-button").classList.add("show");
            document.getElementById("upload-warning-button").classList.remove("hide");
        } else {
            document.getElementById("upload-warning-button").classList.add("hide");
            document.getElementById("upload-warning-button").classList.remove("show");
        }
        buttonA = document.getElementById('approval-button');
            // Toggle button text and status
            if (data.isApproved == true) {
                buttonA.textContent = "Revoke";
                buttonA.classList.remove('approve');
                buttonA.classList.add('revoke');
                buttonA.setAttribute("onclick", "approveButton(this, 'revoke')");
            } else {
                buttonA.textContent = "Approve";
                buttonA.classList.add('approve');
                buttonA.classList.remove('revoke');

                buttonA.setAttribute("onclick", "approveButton(this, 'approve')");
            }
    })
    .catch(error => console.error("Error fetching approval status:", error));
}
setInterval(updateApprovalStatus, 5000);
audioUpload.addEventListener("change", (event) => {
    control_flag = 'upl';
    const file = event.target.files[0];
    if (!file) {
        console.error("No file selected.");
        return;
    }
    UploadBlob=file;
    UploadAudioURL = URL.createObjectURL(UploadBlob);
    console.log(UploadAudioURL);
    initWaveSurfer(g_rSyncContainer,UploadAudioURL);
    gRSync.style.display="block";
    recordButton.disabled=true;
    uploadButton.disabled=true;
});
function renameAudio(syncId) {
    const inputField = document.getElementById(`rename-audio-${syncId}`);
    const newName = inputField.value.trim(); // Get new name
    
    if (!newName) {
        alert("Name cannot be empty!");
        return;
    }

    fetch("/rename_audio/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken() // Ensure CSRF token is included
        },
        body: JSON.stringify({ syncId: syncId, newName: newName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the displayed name
            document.querySelector(`#audio-name-${syncId}`).textContent = newName;
            console.log(`Renamed to: ${newName}`);
        } else {
            alert("Failed to rename: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}
document.getElementById("messageInput").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        if (event.shiftKey) {
            // Shift + Enter: Insert a new line
            event.preventDefault(); // Prevents the default behavior (which might submit the form)
            this.value += "\n"; // Adds a new line inside the input field
        } else {
            // Enter (without Shift): Send the message
            event.preventDefault(); // Prevents accidental line breaks
            document.getElementById("sendButton").click(); // Triggers the send button
        }
    }
});
function fetchTempData() {
    fetch(`/fetch-temp-data?collabId=${collabId}`) 
        .then(response => response.json())
        .then(data => {
            if (data.temp_thumbnail) {
                document.getElementById('upload-tn-img').src = data.temp_thumbnail;
            }
            if (data.temp_caption) {
                document.getElementById('caption').placeholder = data.temp_caption;
                document.getElementById('collab-title').innerText = data.temp_caption;
            }
            if (data.temp_descr) {
                document.getElementById('description').placeholder = data.temp_descr;
            }
            if (data.temp_mediaType) {
                document.getElementById('mType').placeholder = data.temp_mediaType;
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}

setInterval(fetchTempData, 5000);