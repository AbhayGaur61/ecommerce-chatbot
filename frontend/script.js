document.getElementById('send-btn').addEventListener('click', handleUserInput);
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        handleUserInput();
    }
});

const API_BASE_URL = 'http://127.0.0.1:5000';
const responseArea = document.getElementById('response-area');

async function handleUserInput() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput) return;

    // Display user's question as a user message bubble
    addMessage(userInput, 'user-message');
    document.getElementById('user-input').value = '';

    // --- Intent Recognition Logic ---
    const lowerCaseInput = userInput.toLowerCase();
    const orderIdMatch = lowerCaseInput.match(/(\d+)/);

    if (lowerCaseInput.includes("top") && lowerCaseInput.includes("products")) {
        await getTopProducts();
    } else if ((lowerCaseInput.includes("status") || lowerCaseInput.includes("order")) && orderIdMatch) {
        const orderId = orderIdMatch[0];
        await getOrderStatus(orderId);
    } else if (lowerCaseInput.includes("how many") || lowerCaseInput.includes("stock")) {
        const productName = userInput.replace(/how many|stock of|are left in stock\??/gi, "").trim();
        await getStockLevel(productName);
    } else {
        addMessage("Sorry, I don't understand that. Try asking about 'top products', 'order status', or 'stock levels'.", 'bot-message');
    }
}

// --- Functions to call API and display responses ---

async function getTopProducts() {
    const response = await fetch(`${API_BASE_URL}/top_products`);
    const data = await response.json();
    
    let html = '<strong>Here are the top 5 most sold products:</strong><ul>';
    data.forEach(item => {
        html += `<li>${item.name} (Sold: ${item.sales_count})</li>`;
    });
    html += '</ul>';
    addMessage(html, 'bot-message');
}

async function getOrderStatus(orderId) {
    const response = await fetch(`${API_BASE_URL}/order_status/${orderId}`);
    const data = await response.json();

    let message;
    if (data.error) {
        message = data.error;
    } else {
        message = `The status of order #${data.order_id} is <strong>${data.status}</strong>.`;
    }
    addMessage(message, 'bot-message');
}

async function getStockLevel(productName) {
    const encodedProductName = encodeURIComponent(productName);
    const response = await fetch(`${API_BASE_URL}/stock_level?product=${encodedProductName}`);
    const data = await response.json();

    let message;
    if (data.stock_level !== undefined) {
         message = `There are <strong>${data.stock_level}</strong> units of "${data.product_name}" left in stock.`;
    } else {
        message = "Sorry, I couldn't find the stock for that product.";
    }
    addMessage(message, 'bot-message');
}

/**
 * A helper function to add a new message to the chat window.
 * @param {string} text - The message text (can be HTML).
 * @param {string} type - The class name for the message ('user-message' or 'bot-message').
 */
function addMessage(text, type) {
    const messageElement = document.createElement('p');
    messageElement.classList.add('message', type);
    messageElement.innerHTML = text;
    responseArea.appendChild(messageElement);
    responseArea.scrollTop = responseArea.scrollHeight; // Auto-scroll to the latest message
}