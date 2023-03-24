
// ----- COUNTER ----- //

const counter = document.querySelectorAll('.counter_value');
const speed = 20; // The lower the slower
counter.forEach(counter_value => {
    const updateCount = () => {
        const target = +counter_value.getAttribute('data-bs-target');
        const count = +counter_value.innerText;
        const inc = target / speed;
        // Check if target is reached
        if (count < target) {
            // Add inc to count and output in counter_value
            counter_value.innerText = (count + inc).toFixed(0);
            // Call function every ms
            setTimeout(updateCount, 5);
        } else {
            counter_value.innerText = target;
        }
    };
    updateCount();
});