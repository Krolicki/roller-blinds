const rollUpButton = document.getElementById('roll-up')
const rollDownButton = document.getElementById('roll-down')
const abortButton = document.getElementById('abort')
const stepsField = document.getElementById('steps')
const progressBar = document.querySelector('.progress-bar')

const makeRequest = (action) => {
	console.log(action)
	const request = new XMLHttpRequest()
				request.open('POST', `/${action}`)
				request.onload = () => {
						const response = request
						console.log(response)
						getRollProgress()
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
			if(currentStep.direction === 'up' && !rollUpButton.classList.contains('activeAction')){
				rollUpButton.classList.add('activeAction')
				rollDownButton.classList.add('disabledButton')
				if(rollDownButton.classList.contains('activeAction'))
					rollDownButton.classList.remove('activeAction')
			}
			if(currentStep.direction === 'down' && !rollDownButton.classList.contains('activeAction')){
				rollDownButton.classList.add('activeAction')
				rollUpButton.classList.add('disabledButton')
				if(rollUpButton.classList.contains('activeAction'))
					rollUpButton.classList.remove('activeAction')
			}
		}
		else{
			if(currentStep.step == 0)
				stepsField.innerHTML = 'Otwarte'
			else if(currentStep.step == maxStep)
				stepsField.innerHTML = 'Zamknięte'
			else{
				stepsField.innerHTML = `Otwarcie: ${progress}%`
			}
			if(rollUpButton.classList.contains('activeAction'))
				rollUpButton.classList.remove('activeAction')
			if(rollUpButton.classList.contains('disabledButton'))
				rollUpButton.classList.remove('disabledButton')
			if(rollDownButton.classList.contains('activeAction'))
				rollDownButton.classList.remove('activeAction')
			if(rollDownButton.classList.contains('disabledButton'))
				rollDownButton.classList.remove('disabledButton')
		}
}

rollUpButton.addEventListener("click", () => {
			makeRequest('roll-up')
})
rollDownButton.addEventListener("click", () => {
			makeRequest('roll-down')
})
abortButton.addEventListener("click", () => {
			makeRequest('abort')
})
//document.querySelector('.buttons-wraper').querySelectorAll('button')forEach(button => {
		//button.addEventListener("click", () => {
			//makeRequest(button.id)
			//getRollProgress()
		//})
//})
getRollProgress()
