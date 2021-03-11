const canvas = document.getElementById('canvas')
const ctx = canvas.getContext('2d')

const toggleMouseDragSpawnButton = document.getElementById('toggleBitDragSpawn')

const sandSelector = document.getElementById('sandSelector')
const dirtSelector = document.getElementById('dirtSelector')
const smokeSelector = document.getElementById('smokeSelector')
const barrierSelector = document.getElementById('barrierSelector')

let grid = []
let bitManager

let mouseX, mouseY

let shouldMouseDragSpawn = false;

let currentSelectedBit = sandSelector;

function init() {
    for(let x = 0; x < 100; x++) {
        grid[x] = [];
        for(let y = 0; y < 100; y++) {
            grid[x][y] = null;
        }
    }
    bitManager = new BitManager(grid, ctx)
    gameLoop()

    // let modifiers = {
    //     HAS_GRAVITY: true,
    //     WEIGHT: 50,
    //     COLOR: '#FFC300',
    //     IS_SAND: true
    // }
    // let testBit = new BitBase(0, 0, modifiers)
    // bitManager.SpawnBit(1, 1, testBit)
}

function gameLoop() {
    bitManager.UpdateBits()

    window.requestAnimationFrame(gameLoop)
}

window.addEventListener('mousemove', event => {
    actualX = event.x - canvas.offsetLeft;
    actualY = event.y - canvas.offsetTop;

    mouseX = Math.floor(actualX / 5)
    mouseY = Math.floor(actualY / 5)

    let modifiers;
    let newBit;

    if(shouldMouseDragSpawn && mouseX >= 0 && mouseX <= 99 && mouseY >= 0 && mouseY <= 99) {
        switch(currentSelectedBit) {
            case sandSelector:
                modifiers = {
                    NAME: 'sand',
                    HAS_GRAVITY: true,
                    WEIGHT: 49,
                    COLOR: '#FFC300',
                    IS_SAND: true
                }
                newBit = new BitBase(0, 0, modifiers)
                bitManager.SpawnBit(mouseX, mouseY, newBit)
                break;
            case dirtSelector:
                modifiers = {
                    NAME: 'dirt',
                    HAS_GRAVITY: true,
                    WEIGHT: 75,
                    COLOR: '#a04000',
                    IS_DIRT: true
                }
                newBit = new BitBase(0, 0, modifiers)
                bitManager.SpawnBit(mouseX, mouseY, newBit)
                break;
            case smokeSelector:
                modifiers = {
                    NAME: 'smoke',
                    WEIGHT: 49,
                    COLOR: '#707b7c',
                    IS_SMOKE: true,
                    DOES_FLOAT: true
                }
                newBit = new BitBase(0, 0, modifiers)
                bitManager.SpawnBit(mouseX, mouseY, newBit)
                break;
            case barrierSelector:
                modifiers = {
                    NAME: 'barrier',
                    WEIGHT: 0,
                    COLOR: 'black'
                }
                newBit = new BitBase(0, 0, modifiers)
                bitManager.SpawnBit(mouseX, mouseY, newBit)
                break;
        }
    }
})

window.addEventListener('mousedown', event => {
    shouldMouseDragSpawn = true;

    let modifiers;
    let newBit;
})

window.addEventListener('contextmenu', event => {
    bitManager.RemoveBit(mouseX, mouseY)

    event.preventDefault();
}, false);

window.addEventListener('mouseup', event => {
    shouldMouseDragSpawn = false;
})

sandSelector.addEventListener('click', event=> {
    currentSelectedBit = sandSelector;
})

dirtSelector.addEventListener('click', event=> {
    currentSelectedBit = dirtSelector;
})

smokeSelector.addEventListener('click', event => {
    currentSelectedBit = smokeSelector;
})

barrierSelector.addEventListener('click', event => {
    currentSelectedBit = barrierSelector;
})

init()