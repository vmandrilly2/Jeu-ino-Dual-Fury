import pygame
import sys
from settings import *
from src.player import Player
from src.manager import GameManager, ParticleSystem
from src.ui import UI, SkillSelectionUI, MainMenu

class Game:
    def __init__(self):
        pygame.init()
        
        # Set up display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dual Fury - Cooperative Survival Game")
        
        # Clock for FPS
        self.clock = pygame.time.Clock()
        
        # Game components
        self.game_manager = GameManager()
        self.particle_system = ParticleSystem()
        
        # UI components
        self.ui = UI()
        self.skill_selection_ui = SkillSelectionUI()
        self.main_menu = MainMenu()
        
        # Players
        self.players = []
        
        # Game state
        self.running = True
        
    def create_players(self):
        """Create the two players"""
        player1 = Player(1, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        player2 = Player(2, 3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.players = [player1, player2]
        
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Handle different game states
            if self.game_manager.game_state == GAME_STATE_MENU:
                menu_action = self.main_menu.handle_input(event)
                if menu_action == 'start_game':
                    self.start_new_game()
                elif menu_action == 'quit':
                    self.running = False
                    
            elif self.game_manager.game_state == GAME_STATE_SKILL_SELECTION:
                selected_skill = self.skill_selection_ui.handle_input(event)
                if selected_skill:
                    self.game_manager.complete_skill_selection(selected_skill)
                    self.skill_selection_ui.hide()
                    
            elif self.game_manager.game_state == GAME_STATE_GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.start_new_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.game_manager.game_state = GAME_STATE_MENU
                        
            # Global controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_manager.game_state == GAME_STATE_PLAYING:
                        self.game_manager.game_state = GAME_STATE_MENU
                    elif self.game_manager.game_state == GAME_STATE_MENU:
                        self.running = False
                        
    def start_new_game(self):
        """Start a new game"""
        self.create_players()
        self.game_manager.start_new_game()
        self.particle_system = ParticleSystem()
        
    def update(self, dt):
        """Update game state"""
        if self.game_manager.game_state == GAME_STATE_PLAYING:
            # Update players
            keys_pressed = pygame.key.get_pressed()
            for i, player in enumerate(self.players):
                other_player = self.players[1 - i] if len(self.players) > 1 else None
                player.update(dt, keys_pressed, other_player)
                
            # Update game manager
            self.game_manager.update(dt, self.players)
            
            # Update particle system
            self.particle_system.update(dt)
            
            # Check for skill selection trigger
            if self.game_manager.game_state == GAME_STATE_SKILL_SELECTION:
                if self.game_manager.skill_selection_player:
                    self.skill_selection_ui.show(self.game_manager.skill_selection_player)
                    
    def draw(self):
        """Draw everything"""
        self.screen.fill(BLACK)
        
        if self.game_manager.game_state == GAME_STATE_MENU:
            self.main_menu.draw(self.screen)
            
        elif self.game_manager.game_state in [GAME_STATE_PLAYING, GAME_STATE_SKILL_SELECTION]:
            # Draw game world
            self.draw_game_world()
            
            # Draw UI overlays
            if self.game_manager.is_wave_break():
                self.ui.draw_wave_break(
                    self.screen, 
                    self.game_manager.current_wave,
                    self.game_manager.get_wave_break_time_remaining()
                )
                
            # Draw skill selection UI
            if self.game_manager.game_state == GAME_STATE_SKILL_SELECTION:
                self.skill_selection_ui.draw(self.screen)
                
        elif self.game_manager.game_state == GAME_STATE_GAME_OVER:
            # Draw game world (faded)
            self.draw_game_world()
            
            # Draw game over screen
            self.ui.draw_game_over(self.screen, self.game_manager.current_wave - 1)
            
        pygame.display.flip()
        
    def draw_game_world(self):
        """Draw the main game world"""
        # Draw background grid (optional)
        self.draw_background_grid()
        
        # Draw XP orbs
        for orb in self.game_manager.xp_orbs:
            orb.draw(self.screen)
            
        # Draw enemies
        for enemy in self.game_manager.enemies:
            enemy.draw(self.screen)
            
        # Draw players
        for player in self.players:
            if player.is_alive:
                player.draw(self.screen)
            else:
                # Draw dead player with transparency
                dead_surface = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
                dead_surface.fill(GRAY)
                dead_surface.set_alpha(100)
                self.screen.blit(dead_surface, player.rect)
                
        # Draw particles
        self.particle_system.draw(self.screen)
        
        # Draw UI
        if len(self.players) >= 1:
            self.ui.draw_player_hud(self.screen, self.players[0], 'left')
        if len(self.players) >= 2:
            self.ui.draw_player_hud(self.screen, self.players[1], 'right')
            
        # Draw wave info
        if self.game_manager.wave_active:
            enemies_remaining = self.game_manager.get_enemies_remaining()
            self.ui.draw_wave_info(self.screen, self.game_manager.current_wave, enemies_remaining)
        else:
            self.ui.draw_wave_info(self.screen, self.game_manager.current_wave)
            
        # Draw debug info (optional)
        # self.game_manager.draw_debug_info(self.screen, self.ui.small_font)
        
    def draw_background_grid(self):
        """Draw a subtle background grid"""
        grid_size = 50
        grid_color = (20, 20, 20)  # Very dark gray
        
        # Vertical lines
        for x in range(0, SCREEN_WIDTH, grid_size):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, SCREEN_HEIGHT))
            
        # Horizontal lines
        for y in range(0, SCREEN_HEIGHT, grid_size):
            pygame.draw.line(self.screen, grid_color, (0, y), (SCREEN_WIDTH, y))
            
    def run(self):
        """Main game loop"""
        while self.running:
            # Calculate delta time
            dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds
            
            # Handle events
            self.handle_events()
            
            # Update game
            self.update(dt)
            
            # Draw everything
            self.draw()
            
        pygame.quit()
        sys.exit()


def main():
    """Main function"""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()