// Variables

const chatRoom = document.getElementById("room_uuid").textContent.replaceAll('"', '');
const chatName = document.getElementById("user_name").textContent.replaceAll('"', '');
const chatAgent = document.getElementById("user_id").textContent.replaceAll('"', '');
let chatSocket = null;

// Elements

const chatLogElement = document.querySelector("#chat_log");
const chatInputElement = document.querySelector("#chat_message_input");
const chatSubmitElement = document.querySelector("#chat_message_submit");

console.log(chatName)

// Functions

const scrollBottom = () => {
    chatLogElement.scrollTo({
        top: chatLogElement.scrollHeight,
        behavior: "smooth",
    })
}

const sendMessage = () => {
    const data = {
        type: "message",
        message: chatInputElement.value,
        name: chatName,
        agent: chatAgent,
    }
    if (chatInputElement.value) {
        chatSocket.send(JSON.stringify(data));
        chatInputElement.value = '';
    }
}

const onChatMessage = (data) => {
    console.log(data.agent);
    if (data.type == "chat_message") {
        if (!data.agent) {
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
                        <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                            <p class="text-sm">${data.message}</p>
                        </div>
                        <span class="text-xs text-gray-500 leading-none">${data.created_at} ago</span>
                    </div>
                    <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>
                </div>`;
        }
    }
    scrollBottom();
}


// Web Socket
const url = `ws://${window.location.host}/ws/${chatRoom}/`;
chatSocket = new WebSocket(url);



chatSocket.onmessage = (event) => {
    onChatMessage(JSON.parse(event.data))
}

chatSocket.onopen = (event) => {
    scrollBottom();
    console.log("chat open", event);
}

chatSocket.onclose = (event) => {
    console.error(event);
}


chatSubmitElement.addEventListener('click', () => {
    sendMessage();
})

chatInputElement.addEventListener("keyup", (event) => {
    if (event.keyCode === 13) {
        sendMessage();
    }
})