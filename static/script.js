console.log("start")

const makeRequest = (action) => {
	console.log(action)
	const request = new XMLHttpRequest()
				request.open('POST', `/${action}`)
				request.onload = () => {
						const response = request.responseText
						document.getElementById('steps').innerHTML = response
				}; 
				request.send()
}


document.querySelectorAll('button').forEach(button => {
		button.addEventListener("click", () => makeRequest(button.id))
})
