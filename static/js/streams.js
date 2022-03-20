let client = AgoraRTC.createClient({mode:'rtc', codec:'vp8',})

let config = {
    appid:'0ccebb6c713a45bcb5ae0291c277efe3',
    token:'0060ccebb6c713a45bcb5ae0291c277efe3IABzTYLvZP8yxg6Zubn4hGAUpLNi8PStVKIgIMrXbhmBQWTNKL8AAAAAEAAWylBUHIUSYgEAAQAehRJi',
    uid:null,
    channel:'main',
}

let localTracks = {
    audioTrack:null,
    videoTrack:null,
}


let remoteTracks = {}

document.getElementById('join-btn').addEventListener('click', async ()=> {
    console.log('User Joined stream')
    await joinStreams()
})

let joinStreams = async () => {

    client.on("user-published", handleUserJoined);
    client.on("user-left", handleUserLeft);

    [config.uid, localTracks.audioTrack, localTracks.videoTrack] = await Promise.all([
        client.join(config.appid, config.channel, config.token ||null, config.uid ||null),
        AgoraRTC.createMicrophoneAudioTrack(),
        AgoraRTC.createCameraVideoTrack(),
    ])


    let videoPlayer = `<div  class="video-container" id="user-container-${config.uid}">
                         <p class="user-uid">${config.uid}</p>
                         <div class="video-player" id="stream-${config.uid}"></div>
                       </div>`

    document.getElementById('video-streams').insertAdjacentHTML('beforeend', videoPlayer)
    localTracks.videoTrack.play(`stream-${config.uid}`)

    await client.publish([localTracks.audioTrack, localTracks.videoTrack])


}

let handleUserLeft = async () => {
    console.log('User left')
}

let handleUserJoined = async (user, mediaType) => {
    console.log('User join')
    remoteTracks[user.uid] = user

    await client.subscribe(user, mediaType)

    if (mediaType === 'video'){
        let videoPlayer = `<div  class="video-container" id="user-container-${user.uid}">
                         <p class="user-uid">${user.uid}</p>
                         <div class="video-player" id="stream-${user.uid}"></div>
                       </div>`

        document.getElementById('video-streams').insertAdjacentHTML('beforeend', videoPlayer)
        user.videoTrack.play(`stream-${user.uid}`);
    }

    if(mediaType === 'audio'){
        user.audioTrack.play();
    }

}