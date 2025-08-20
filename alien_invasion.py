import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((800, 600))
        self.fullscreen = False
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        # Initialize the background color
        self.bg_color = (230, 230, 230)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
            """Respond to keypresses and mouse events."""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                     self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                        self._check_keyup_events(event)

    def _check_keydown_events(self, event):
            """Respond to key presses."""
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_ESCAPE:  
                sys.exit() 
            elif event.key == pygame.K_SPACE:
                 self._fire_bullet() 
            elif event.key == pygame.K_f:
            # Toggle fullscreen
                self.fullscreen = not self.fullscreen
                if self.fullscreen:
                    self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    self.screen = pygame.display.set_mode((800, 600))

            # Update settings
                self.settings.screen_width = self.screen.get_width()
                self.settings.screen_height = self.screen.get_height()
            # Update ship's screen_rect to match new screen
                self.ship.screen_rect = self.screen.get_rect()
                self.ship.center_ship()
            # Clear and recreate fleet
                self.aliens.empty()
                self._create_fleet()
                
    
    def _check_keyup_events(self, event):
            """Respond to key releases."""
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False 


    def _fire_bullet(self):
         """Create a new bullet and add it to the bullets group."""               
         if len(self.bullets) < self.settings.bullets_allowed:
             new_bullet = Bullet(self)
             self.bullets.add(new_bullet)

    def _update_bullets(self):
        """update the position of bullets and get rid of old ones"""        
        self.bullets.update()
        for bullet in self.bullets.copy():
          if bullet.rect.bottom <= 0:
            self.bullets.remove(bullet)  
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):    
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Destroy existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.fleet_direction *= -1

    def _create_fleet(self):
        """Create a fleet of aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y  = alien_width, alien_height
        while current_y < (self.settings.screen_height -3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width  # Adjust spacing between aliens
            
            current_x = alien_width  # Reset x position for the next row
            current_y += alien_height  # Move down to the next row
        # Add the last alien in the row
            self.aliens.add(alien)

    def _create_alien(self, x_position, y_position):
         new_alien = Alien(self)
         new_alien.x = x_position
         new_alien.rect.x = x_position
         new_alien.rect.y = y_position
         self.aliens.add(new_alien)

    def _update_aliens(self):
         self.aliens.update()
         self._check_fleet_edges()
         if pygame.sprite.spritecollideany(self.ship, self.aliens):
              print("Ship hit by alien!")


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1             
        

      

    def _update_screen(self):
            self.screen.fill(self.settings.bg_color)
            for bullet in self.bullets.sprites():
                 bullet.draw_bullet()
            self.ship.blitme()
            self.aliens.draw(self.screen)
            pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()                     