// Elements
const chatElement = document.querySelector("#chat");
const chatIconElement = document.querySelector("#chat_icon");
const chatWelcomeElement = document.querySelector("#chat_welcome");
const chatJoinElement = document.querySelector("#chat_join");
const chatOpenElement = document.querySelector("#chat_open");
const chatRoomElement = document.querySelector("#chat_room");
const chatNameElement = document.querySelector("#chat_name");
const chatLogElement = document.querySelector("#chat_log");
const chatInputElement = document.querySelector("#chat_message_input");
const chatSubmitElement = document.querySelector("#chat_message_submit");


// Variables
let chatSocket = null
let chatName = '';
let chatUrl = window.location.href;
let chatRoomUuid = Math.random().toString(36).slice(2, 12);



// Functions

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');



const sendMessage = () => {
    const data = {
        type: "message",
        message: chatInputElement.value,
        name: chatName,
    }
    if (chatInputElement.value) {
        chatSocket.send(JSON.stringify(data));
        chatInputElement.value = '';
    }

}


const onChatMessage = (data) => {
    console.log(data)
    if (data.type == "chat_message") {
        if (data.agent) {
            chatLogElement.innerHTML += `
                <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-start">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>
                    <div>
                        <div class="bg-gray-300 p-3 rounded-l-lg rounded-br-lg">
                            <p class="text-sm">${data.message}</p>
                        </div>
                        <span class="text-xs text-gray-500 leading-none">${data.created_at} ago</span>
                    </div>
                </div>`;

        } else {
            chatLogElement.innerHTML += `
                <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
                    <div>
                        <div class="bg-blue-300 p-3 rounded-l-lg rounded-br-lg">
                            <p class="text-sm">${data.message}</p>
                        </div>
                        <span class="text-xs text-gray-500 leading-none">${data.created_at} ago</span>
                    </div>
                    <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>
                </div>`;
        }
    } else if (data.type == "user_update") {
        chatLogElement.innerHTML += `
        <p class="mt-2">
            ${data.user} has joined the chat
        </p>
        `
    }
    scrollBottom();
}

const joinChatRoom = async () => {
    chatName = chatNameElement.value;
    try {
        await fetch(`/api/create-room/${chatRoomUuid}/`, {
            method: 'POST',
            headers: {
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({ name: chatName, url: chatUrl })
        })
            .then(response => response.json())
            .then(data => console.log(data))
    } catch (error) {
        throw new Error(`Error:${error}`)
    }

    const url = `ws://${window.location.host}/ws/${chatRoomUuid}/`;
    chatSocket = new WebSocket(url);

    chatSocket.onmessage = (event) => {
        onChatMessage(JSON.parse(event.data));
    }
    chatSocket.onopen = (event) => {
        scrollBottom();
        console.log(`Chat Socket is opend ${event}`)
    }
    chatSocket.onclose = (event) => {
        console.log("Chat closed", event);
    }
}

const scrollBottom = () => {
    chatLogElement.scrollTo({
        top: chatLogElement.scrollHeight,
        behavior: "smooth",
    })
}




//EventListener
chatOpenElement.addEventListener('click', () => {
    chatIconElement.classList.add('hidden');
    chatWelcomeElement.classList.remove('hidden');
});



chatJoinElement.addEventListener('click', () => {
    chatWelcomeElement.classList.add('hidden');
    chatRoomElement.classList.remove('hidden');
    joinChatRoom();
});

chatSubmitElement.addEventListener('click', () => {
    sendMessage();
})

chatInputElement.addEventListener("keyup", (e) => {
    console.log(e.KeyCode);
    if (e.KeyCode == 13) {
        sendMessage();
    }
})