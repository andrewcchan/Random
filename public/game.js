console.log("Lane Zero is running!");

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Set canvas dimensions
canvas.width = 800;
canvas.height = 600;

// Game Constants
const LANE_WIDTH_PERCENT = 0.4;

// Game Objects
const bullets = [];
const enemies = [];

const barricade = {
    x: 0,
    y: canvas.height - 40,
    width: canvas.width,
    height: 40,
    color: '#663300',
    health: 100,
    draw(ctx) {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.width, this.height);

        // Draw health bar
        const healthBarWidth = this.width * 0.8;
        const healthBarHeight = 10;
        const healthBarX = this.x + (this.width - healthBarWidth) / 2;
        const healthBarY = this.y + 5;

        // Background
        ctx.fillStyle = 'red';
        ctx.fillRect(healthBarX, healthBarY, healthBarWidth, healthBarHeight);

        // Current health
        ctx.fillStyle = 'green';
        ctx.fillRect(healthBarX, healthBarY, healthBarWidth * (this.health / 100), healthBarHeight);
    }
};

const player = {
    width: 50,
    height: 80,
    color: '#00cc66',
    currentLane: 'left',
    get x() {
        const laneWidth = canvas.width * LANE_WIDTH_PERCENT;
        if (this.currentLane === 'left') {
            return laneWidth / 2 - this.width / 2;
        } else {
            return canvas.width - (laneWidth / 2) - this.width / 2;
        }
    },
    y: barricade.y - 80, // Positioned on top of the barricade
    draw(ctx) {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }
};

function drawLanes(ctx) {
    const laneWidth = canvas.width * LANE_WIDTH_PERCENT;
    ctx.fillStyle = '#333';
    // Left Lane
    ctx.fillRect(0, 0, laneWidth, canvas.height);
    // Right Lane
    ctx.fillRect(canvas.width - laneWidth, 0, laneWidth, canvas.height);
}


// Game State
let isGameOver = false;
let animationFrameId;
let enemySpawnerId;

// Game logic will go here
function gameLoop() {
    if (isGameOver) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'white';
        ctx.font = '50px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('Game Over', canvas.width / 2, canvas.height / 2);
        cancelAnimationFrame(animationFrameId);
        return;
    }

    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw background
    ctx.fillStyle = '#222';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw game elements
    drawLanes(ctx);
    barricade.draw(ctx);
    player.draw(ctx);

    // Update and draw bullets
    for (let i = bullets.length - 1; i >= 0; i--) {
        const bullet = bullets[i];
        bullet.y -= bullet.speed;
        ctx.fillStyle = bullet.color;
        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);

        // Remove bullet if it's off-screen
        if (bullet.y + bullet.height < 0) {
            bullets.splice(i, 1);
        }
    }

    // Update and draw enemies
    for (let i = enemies.length - 1; i >= 0; i--) {
        const enemy = enemies[i];
        enemy.y += enemy.speed;
        ctx.fillStyle = enemy.color;
        ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);

        // Check for collision with barricade
        if (enemy.y + enemy.height > barricade.y) {
            enemies.splice(i, 1);
            barricade.health -= 10;
            if (barricade.health <= 0) {
                isGameOver = true;
            }
        }
    }

    // Collision detection
    for (let i = bullets.length - 1; i >= 0; i--) {
        for (let j = enemies.length - 1; j >= 0; j--) {
            const bullet = bullets[i];
            const enemy = enemies[j];

            if (bullet && enemy &&
                bullet.x < enemy.x + enemy.width &&
                bullet.x + bullet.width > enemy.x &&
                bullet.y < enemy.y + enemy.height &&
                bullet.y + bullet.height > enemy.y) {

                bullets.splice(i, 1);
                enemies.splice(j, 1);
            }
        }
    }


    animationFrameId = requestAnimationFrame(gameLoop);
}

function spawnEnemy() {
    if (isGameOver) {
        clearInterval(enemySpawnerId);
        return;
    }
    const laneWidth = canvas.width * LANE_WIDTH_PERCENT;
    const lane = Math.random() < 0.5 ? 'left' : 'right';
    const x = lane === 'left'
        ? laneWidth / 2 - 25
        : canvas.width - (laneWidth / 2) - 25;

    enemies.push({
        x: x,
        y: -50, // Start off-screen
        width: 50,
        height: 50,
        color: 'red',
        speed: 2
    });
}

// Start the game loop
gameLoop();

// Start spawning enemies
enemySpawnerId = setInterval(spawnEnemy, 2000);

// Player Input
window.addEventListener('keydown', (e) => {
    if (isGameOver) return;
    if (e.key === 'ArrowLeft') {
        player.currentLane = 'left';
    } else if (e.key === 'ArrowRight') {
        player.currentLane = 'right';
    }
});

window.addEventListener('click', (e) => {
    if (isGameOver) return;
    // Create a new bullet
    bullets.push({
        x: player.x + player.width / 2 - 5,
        y: player.y,
        width: 10,
        height: 30,
        color: 'yellow',
        speed: 7
    });
});
