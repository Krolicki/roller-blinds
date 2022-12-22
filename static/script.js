const rollUpButton = document.getElementById('roll-up')
const rollDownButton = document.getElementById('roll-down')
const abortButton = document.getElementById('abort')
const stepsField = document.getElementById('steps')
const progressBar = document.querySelector('.progress-bar')

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
		let progress = ((currentStep.step / maxStep) * 100).toFixed(0)
		progressBar.style.height = `${progress}%`
		if(currentStep.move == true){
			stepsField.innerHTML = `Otwarcie: ${progress}%`
			progressBar.style.height = `${progress}%`
			setTimeout(getRollProgress, 2000);
		}
		else{
			if(currentStep.step == 0)
				stepsField.innerHTML = 'Otwarte'
			else if(currentStep.step == maxStep)
				stepsField.innerHTML = 'Zamknięte'
			else{
				stepsField.innerHTML = `Otwarcie: ${progress}%`
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
