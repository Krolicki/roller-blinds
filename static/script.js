const rollUpButton = document.getElementById('roll-up')
const rollDownButton = document.getElementById('roll-down')
const abortButton = document.getElementById('abort')
const stepsField = document.getElementById('steps')

let rollInterval = null

const makeRequest = (action) => {
	console.log(action)
	const request = new XMLHttpRequest()
				request.open('POST', `/${action}`)
				request.onload = () => {
						const response = request
						console.log(response)
				}; 
				request.send()
}

const getSteps = async () => {
		let currentStep = await fetch('/steps')
		.then(response => {
				if (response.ok)
						return response.json()
				throw response
		})
		.catch((err)=>{
			console.log(err)
		})
		console.log(currentStep)
		return currentStep
}

const getRollProgress = async () =>{
		let currentStep = await getSteps()
				console.log(currentStep)
		if(currentStep.move == true){
			let progress = ((currentStep.step / maxStep) * 100).toFixed(0)
			stepsField.innerHTML = `Stopień otwarcia: ${progress}%`
			setTimeout(getRollProgress, 2000);
		}
		else{
			if(currentStep.step == 0)
				stepsField.innerHTML = 'Status: Otwarte'
			else if(currentStep.step == maxStep)
				stepsField.innerHTML = 'Status: Zamknięte'
			else{
				let progress = ((currentStep.step / maxStep) * 100).toFixed(0)
				stepsField.innerHTML = `Stopień otwarcia: ${progress}%`
			}
		}
}

rollUpButton.addEventListener("click", () => {
			makeRequest('roll-up')
			getRollProgress()
})
rollDownButton.addEventListener("click", () => {
			makeRequest('roll-down')
			getRollProgress()
})
abortButton.addEventListener("click", () => {
			makeRequest('abort')
			getRollProgress()
})
//document.querySelector('.buttons-wraper').querySelectorAll('button')forEach(button => {
		//button.addEventListener("click", () => {
			//makeRequest(button.id)
			//getRollProgress()
		//})
//})
getRollProgress()
