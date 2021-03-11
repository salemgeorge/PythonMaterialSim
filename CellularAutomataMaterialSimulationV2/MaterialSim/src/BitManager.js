class BitManager {
    grid;
    ctx;
    constructor(grid, ctx) {
        this.grid = grid
        this.ctx = ctx
    }

    UpdateBits() {
        this.ctx.clearRect(0, 0, 500, 500)
        for(let x = 99; x > 0; x--) {
            for(let y = 99; y > 0; y--) {
                if(!grid[x][y]) continue;
                
                // Assigning Vars
                let bitToUpdate = grid[x][y]
                let bitPos = {x, y, didMove: false}
                let bitBelow = this.GetBit(x, y + 1)
                let bitAbove = this.GetBit(x, y - 1)

                // Handling Components
                if(bitToUpdate.modifiers.IS_SAND) {
                    if(grid[bitPos.x][bitPos.y]) {
                        bitPos = grid[bitPos.x][bitPos.y].HandleSlopePhysics(3)
                    }
                    if(bitPos.didMove) grid[x][y] = null
                }
                if(bitToUpdate.modifiers.IS_DIRT) {
                    if(grid[bitPos.x][bitPos.y]) {
                        bitPos = grid[bitPos.x][bitPos.y].HandleHeightRestricionsPhysics(3)
                    }
                    if(bitPos.didMove) grid[x][y] = null
                }
                if(bitToUpdate.modifiers.IS_SMOKE) {
                    if(grid[bitPos.x][bitPos.y]) {
                        bitPos = grid[bitPos.x][bitPos.y].HandleSmokePhysics()
                    }
                    if(bitPos.didMove) grid[x][y] = null
                }
                if(bitToUpdate.modifiers.HAS_GRAVITY) {
                    if(!bitBelow && grid[bitPos.x][bitPos.y]) {
                        bitPos = grid[bitPos.x][bitPos.y].ApplyGravity()
                        grid[bitPos.x][bitPos.y].modifiers.IS_FALLING = true
                        if(bitPos.didMove) grid[x][y] = null
                    } else if(bitBelow) {
                        if(grid[bitPos.x][bitPos.y])
                            grid[bitPos.x][bitPos.y].modifiers.IS_FALLING = false
                    }
                } else if(bitToUpdate.modifiers.DOES_FLOAT) {
                    if(bitAbove === null && grid[bitPos.x][bitPos.y]) {
                        bitPos = grid[bitPos.x][bitPos.y].FloatUp()
                        // grid[bitPos.x][bitPos.y].modifiers.IS_FALLING = true
                        if(bitPos.didMove) grid[x][y] = null
                    }
                }

                // Drawing
                if(grid[bitPos.x][bitPos.y]) {
                    grid[bitPos.x][bitPos.y].DrawSelf(ctx)
                }
            }
        }
    }

    SpawnBit(x, y, bitToSpawn) {
        if(!grid[x][y]) {
            bitToSpawn.x = x;
            bitToSpawn.y = y;
            grid[x][y] = bitToSpawn;
        }
    }

    GetBit(x, y) {
        return grid[x][y]
    }

    RemoveBit(x, y) {
        if(grid[x][y] || grid[x][y] === null) {
            grid[x][y] = null
        }
    }
}