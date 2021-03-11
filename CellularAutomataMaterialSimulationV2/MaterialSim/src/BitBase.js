class BitBase {
    x;
    y;
    modifiers;
    direction;

    constructor(x, y, modifiers) {
        this.x = x;
        this.y = y;
        this.modifiers = modifiers;

        Object.defineProperties(this.modifiers, {
            UPDATE_PROGRESS_TO_MOVE: {
                value: 100,
                writable: false
            },
            CURRENT_UPDATE_PROGRESS: {
                value: 0,
                writable: true
            },
            IS_FALLING: {
                value: true,
                writable: true
            }
        })

        this.direction = {
            LEFT: 'left',
            RIGHT: 'right',
            UP: 'up',
            DOWN: 'down'
        }
    }

    MoveSelf(direction) {
        let x = this.x;
        let y = this.y;

        switch(direction) {
            case this.direction.LEFT:
                grid[x - 1][y] = grid[x][y]
                x--
                break;
            case this.direction.RIGHT:
                grid[x + 1][y] = grid[x][y]
                x++
                break;
            case this.direction.UP:
                grid[x][y - 1] = grid[x][y]
                y--
                break;
            case this.direction.DOWN:
                grid[x][y + 1] = grid[x][y]
                y++
                break;
        }

        this.x = x;
        this.y = y;

        return {x, y, didMove: true}
    }

    DrawSelf(ctx) {
        ctx.fillStyle = this.modifiers.COLOR;
        ctx.fillRect(this.x * 5, this.y * 5, 5, 5)
    }

    ApplyGravity() {
        let mods = this.modifiers

        if(mods.CURRENT_UPDATE_PROGRESS >= mods.UPDATE_PROGRESS_TO_MOVE) {

            let canMove = this.y < 99
            if(canMove) {
                mods.CURRENT_UPDATE_PROGRESS = 0

                this.MoveSelf(this.direction.DOWN)

                this.modifiers = mods

                let x = this.x;
                let y = this.y
                let didMove = true;
                return {x, y, didMove}
            }
            let x = this.x;
            let y = this.y
            let didMove = false;

            return {x, y, didMove}
        }
        mods.CURRENT_UPDATE_PROGRESS += mods.WEIGHT

        this.modifiers = mods

        let x = this.x;
        let y = this.y
        let didMove = false;
        return {x, y, didMove}
    }

    FloatUp() {
        let mods = this.modifiers

        if(mods.CURRENT_UPDATE_PROGRESS >= mods.UPDATE_PROGRESS_TO_MOVE) {

            let canMove = this.y > 1
            if(canMove) {
                mods.CURRENT_UPDATE_PROGRESS = 0

                this.MoveSelf(this.direction.UP)

                this.modifiers = mods

                let x = this.x;
                let y = this.y
                let didMove = true;
                return {x, y, didMove}
            }
            let x = this.x;
            let y = this.y
            let didMove = false;

            return {x, y, didMove}
        }
        mods.CURRENT_UPDATE_PROGRESS += mods.WEIGHT

        this.modifiers = mods

        let x = this.x;
        let y = this.y
        let didMove = false;
        return {x, y, didMove}
    }

    GetBit(x, y) {
        if((x >= 0 && x <= 99) && (y >= 0 && y <= 99)) {
            return grid[x][y]
        } else {
            return undefined
        }
    }

    HandleSlopePhysics(xSlope) {
        // This function makes piles flatter, and wider

        // Assigning Vars
        let mods = this.modifiers
        let x = this.x
        let y = this.y
        let bitBelow = this.GetBit(x, y + 1)
        let dirMoved = {x, y, didMove: false}

        // Checking if were at the bottom of the screen, and if were on top of a bit
        if(y + 1 <= 99 && bitBelow) {
            let bitFarRight;
            let bitFarLeft;

            // Figuring out where we should look for the bit that will cause the toppling
            if(x + xSlope <= 99) {
                bitFarRight = this.GetBit(x + xSlope, y + 1)
            } else {
                bitFarRight = this.GetBit(99 - x, y + 1)
            }

            if(x - xSlope >= 0) {
                bitFarLeft = this.GetBit(x - xSlope, y + 1)
            } else {
                bitFarLeft = this.GetBit(x, y + 1)
            }

            // Taking the gap test, very stressful
            let leftGapTest = bitFarLeft && this.GetBit(x - 1, y + 1) === null
            let rightGapTest = bitFarRight && this.GetBit(x + 1, y + 1) === null

            // If we dont check for a gap, it introduces a gap bug
            // The gap bug is kind of hard to explain, but I'll try my best
            // When we check for a bit, we check xSlope over, and one down.
            // If there is another pile there, then the bit decides to not move.
            // The solution to detect if the bit is part of our pile, and if
            // it is, than we just move it anyways

            if(leftGapTest || rightGapTest) {
                // Now that we know there is a gap, we just need to figure out which side it is on
                if(leftGapTest) {
                    if(this.GetBit(x - 1, y) === null) {
                        this.MoveSelf(this.direction.LEFT)
                        dirMoved.x--;
                        dirMoved.didMove = true
                    }
                } else {
                    if(this.GetBit(x + 1, y) === null) {
                        this.MoveSelf(this.direction.RIGHT)
                        dirMoved.x++;
                        dirMoved.didMove = true
                    }
                }
                //If there is no gap, than just resume normal behaviour
            } else {
                // Toppling Left
                if(bitFarLeft === null && bitFarRight) {
                    if(this.GetBit(x - 1, y) === null) {
                        this.MoveSelf(this.direction.LEFT)
                        dirMoved.x--;
                        dirMoved.didMove = true
                    }
                // Toppling Right
                } else if(bitFarLeft && bitFarRight === null) {
                    if(this.GetBit(x + 1, y) === null) {
                        this.MoveSelf(this.direction.RIGHT)
                        dirMoved.x++;
                        dirMoved.didMove = true
                    }
                // We can topple both dirs, so we just pick a rand one
                } else if(bitFarLeft === null && bitFarRight === null) {
                    let randDir = Math.random()
    
                    if(randDir < 0.5) {
                        if(this.GetBit(x - 1, y) === null) {
                            this.MoveSelf(this.direction.LEFT)
                            dirMoved.x--;
                            dirMoved.didMove = true
                        }
                    } else {
                        if(this.GetBit(x + 1, y) === null) {
                            this.MoveSelf(this.direction.RIGHT)
                            dirMoved.x++;
                            dirMoved.didMove = true
                        }
                    }
                }
            }
            return dirMoved;
        }

        return dirMoved;
    }

    HandleHeightRestricionsPhysics(yHeight) {
        // This function makes piles taller, and thinner
        
        let x = this.x
        let y = this.y
        let bitBelow = this.GetBit(x, y + 1)
        let dirMoved = {x, y, didMove: false}
        
        if(!bitBelow) return dirMoved;

        let bitLeft;
        let bitRight;

        if(y + yHeight <= 99 && x - 1 >= 0 && x + 1 <= 99) {
            bitLeft = this.GetBit(x - 1, y + yHeight)
            bitRight = this.GetBit(x + 1, y + yHeight)
        } else {
            if(y + yHeight > 99) {
                if(x - 1 < 0) bitLeft = undefined
                if(x + 1 > 99) bitRight = undefined
            }
        }
        
        if(bitLeft === null && bitRight) {
            if(this.GetBit(x - 1, y) === null) {
                this.MoveSelf(this.direction.LEFT)
                dirMoved.x--;
                dirMoved.didMove = true
            }
        } else if(bitLeft && bitRight === null) {
            if(this.GetBit(x + 1, y) === null) {
                this.MoveSelf(this.direction.RIGHT)
                dirMoved.x++
                dirMoved.didMove = true
            }
        } else if(bitLeft === null && bitRight === null) {
            let randDir = Math.random()

            if(randDir < 0.5) {
                if(this.GetBit(x - 1, y) === null) {
                    this.MoveSelf(this.direction.LEFT)
                    dirMoved.x--;
                    dirMoved.didMove = true
                }
            } else {
                if(this.GetBit(x + 1, y) === null) {
                    this.MoveSelf(this.direction.RIGHT)
                    dirMoved.x++
                    dirMoved.didMove = true
                }
            }
        }

        return dirMoved;
    }

    HandleSmokePhysics() {
        let x = this.x
        let y = this.y
        let bitAbove = this.GetBit(x, y - 1)
        let dirMoved = {x, y, didMove: false}
        
        if(!bitAbove) return dirMoved;

        let bitLeft = this.GetBit(x - 1, y);
        let bitRight = this.GetBit(x + 1, y);

        if(bitLeft === null && bitRight) {
            if(this.x > 1) {
                this.MoveSelf(this.direction.LEFT)
                dirMoved.x--
                dirMoved.didMove = true
            }
        } else if(bitLeft && bitRight === null) {
            if(this.x < 99) {
                this.MoveSelf(this.direction.RIGHT)
                dirMoved.x++
                dirMoved.didMove = true
            }
        } else if(bitLeft === null && bitRight === null) {
            let randDir = Math.random()
            if(randDir <= 0.7 && bitLeft === null) {
                this.MoveSelf(this.direction.LEFT)
                dirMoved.x--
                dirMoved.didMove = true
            } else if(randDir > 0.3  && bitRight === null) {
                this.MoveSelf(this.direction.RIGHT)
                dirMoved.x++
                dirMoved.didMove = true
            }
        } else if(bitLeft && bitRight) {
            let canBeNeighbours = [
                'smoke'
            ]
        }

        return dirMoved;
    }
}