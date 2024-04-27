export const handleSendPromptConnect = (prompt: string) => {
  const url = "http://127.0.0.1:5000/"; // URL where the Flask app is running
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ user_question: prompt }), // Properly encode and include the prompt in the body
  };

  console.log("Sending request to server with prompt:", prompt); // Debug log for the prompt being sent

  return fetch(url, options)
    .then((response) => {
      console.log("Received response from server"); // Debug log for successful receipt of response
      return response.json(); // Convert the response to JSON
    })
    .then((data) => {
      return data; // Debug log to display the server response
      // Handle the response here, e.g., display it in your React component
    })
    .catch((error) => {
      console.error("Error fetching data:", error); // Debug log for any errors encountered
    });
};

export const handleDeleteMemoryConnect = (prompt: string) => {
  const url = "http://127.0.0.1:5000/clear_history"; // URL where the Flask app is running
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ user_question: prompt }), // Properly encode and include the prompt in the body
  };

  console.log("Sending request to server with prompt:", prompt); // Debug log for the prompt being sent

  return fetch(url, options)
    .then((response) => {
      console.log("Received response from server"); // Debug log for successful receipt of response
      return response.json(); // Convert the response to JSON
    })
    .then((data) => {
      return data; // Debug log to display the server response
      // Handle the response here, e.g., display it in your React component
    })
    .catch((error) => {
      console.error("Error fetching data:", error); // Debug log for any errors encountered
    });
};
