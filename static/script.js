console.log("start")

const makeRequest = (action) => {
	console.log(action)
	const request = new XMLHttpRequest()
				request.open('POST', `/${action}`)
				request.onload = () => {
						const response = request
						console.log(response)
						document.getElementById('steps').innerHTML = response.responseText
				}; 
				request.send()
}


document.querySelectorAll('button').forEach(button => {
		button.addEventListener("click", () => makeRequest(button.id))
})
