export function configureDatalists(inputClassName, createNewOption) {
    document.querySelectorAll("."+inputClassName).forEach((input) => {
        input.addEventListener("input", () => {
            const inputValue = input.value.trim();
            const datalist = document.getElementById(input.dataset.type+"-"+inputClassName);
            const options = datalist.options;
            const hiddenInput = document.getElementById(input.dataset.type+'-'+input.dataset.ref+'-id')

            for (let option of options) {
                if (option.value === inputValue) {
                    hiddenInput.value = option.dataset.id;
                    return;
                }
            }
            
            if (createNewOption) hiddenInput.value = "NEW:"+inputValue
            else hiddenInput.value = ""
        });
    })
}