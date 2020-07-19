// apply 'active' class as appropriate
//
// stage is a number from 1-4 where:
// 1 indicates the order has been received
// 2 indicates the order is being made
// 3 indicates the order is ready for pickup/being delivered
// 4 indicates the order is complete
function setStage(stage) {
    for (let i = 1; i <= stage; i++) {
        document.querySelector('.stage.stage' + i).classList.add('active');

        if (i !== 1) {
            document.querySelector('.joiner.stage' + i).classList.add('active');
        }
    }
}
