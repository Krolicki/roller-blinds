const rollUpButton = document.getElementById('roll-up')
const rollDownButton = document.getElementById('roll-down')
const abortButton = document.getElementById('abort')
const stepsField = document.getElementById('progres-status')
const mainRollersStatus = document.getElementById('main-rollers-status')
const progressBar = document.querySelector('.progress-bar')
const mainScreen = document.querySelector('.main')
const blindsControlScreen = document.querySelector('.blinds-control')
const backArrow = document.querySelector('.left-arrow')
const blindsButton = document.getElementById('blinds-button')

let vh = window.innerHeight * 0.01;
document.documentElement.style.setProperty('--vh', `${vh}px`);

const makeRequest = (action) => {
	stepsField.innerHTML = "Wysyłanie..."
	const request = new XMLHttpRequest()
				request.open('POST', `/${action}`)
				request.onload = () => {
						const response = request
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
		return currentStep
}

const getRollProgress = async () =>{
		let currentStep = await getSteps()
		let progress = ((currentStep.step / maxStep) * 100).toFixed(0)
		progressBar.style.height = `${progress}%`
		if(currentStep.move == true){
			let status = `Zamknięcie: ${progress}%`
			stepsField.innerHTML = status
			mainRollersStatus.innerHTML = status
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
			if(currentStep.step == 0){
				let status = 'Otwarte'
				stepsField.innerHTML = status
				mainRollersStatus.innerHTML = status
			}

			else if(currentStep.step == maxStep){
				let status = 'Zamknięte'
				stepsField.innerHTML = status
				mainRollersStatus.innerHTML = status
			}
			else{
				let status = `Zamknięcie: ${progress}%`
				stepsField.innerHTML = status
				mainRollersStatus.innerHTML = status
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
blindsButton.addEventListener("click", () => {
			mainScreen.classList.add('hide-main')
			blindsControlScreen.classList.add('show-screen')
})
backArrow.addEventListener("click", () => {
			mainScreen.classList.remove('hide-main')
			blindsControlScreen.classList.remove('show-screen')
})
//document.querySelector('.buttons-wraper').querySelectorAll('button')forEach(button => {
		//button.addEventListener("click", () => {
			//makeRequest(button.id)
			//getRollProgress()
		//})
//})
getRollProgress()
