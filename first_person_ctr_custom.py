from ursina import *
from collision_system import *


class CustomFirstPersonController(Entity):
    def __init__(self, terrain, **kwargs):
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=.008, rotation_z=45)
        super().__init__()
        self.speed = 5
        self.height = 2
        self.width = 1 # FIXME
        self.distance = 1 # FIXME
        self.camera_pivot = Entity(parent=self, y=self.height)
        
        
        self.step_hight=2# TEST
        self.feet_ray_hit = False
        self.terrain=terrain#TEST for collision system
        self.direction = Vec3()
        self.debug = False

        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 90
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 1
        self.grounded = False
        self.jump_height = 2
        self.jump_up_duration = .5
        self.fall_after = .35 # will interrupt jump up
        self.jumping = False
        self.air_time = 0


        for key, value in kwargs.items():
            setattr(self, key ,value)

        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))
            if ray.hit:
                self.y = ray.world_point.y


    def horisontal_collisions(self):
        pass

    def update(self):

        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)

        self.direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
            )
        # print(f"self.direction: {self.direction}")
        self.direction = self.direction.normalized()
        # print(f"self.direction normalized: {self.direction}")

        collide_wall(self, self.terrain.td)#TEST NOTE testing collide_wall, before rays, rays can be put inside this 

        #feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, ignore=(self,), distance=self.distance, debug=True)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, ignore=(self,), distance=.5, debug=self.debug)
        #if not feet_ray.hit and not head_ray.hit:
        #body_box2 = boxcast(self.position+Vec3(1,1,1), self.up, distance=self.height-0.5, thickness=(0.2,0.2), ignore=(self,), debug=True)
        body_box = boxcast(self.position+Vec3(0,0.1,0), self.direction, distance=.4, thickness=(0.2,self.height-.1), ignore=(self,), debug=True)#change first thickness param to change width of the box
        if not head_ray.hit and not self.feet_ray_hit and not body_box.hit:
            self.position += self.direction * self.speed * time.dt


        if self.gravity:
            # gravity
            ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))
            # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=(self,))

            if ray.distance <= self.height+.1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                    self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            # if not on ground and not on way up in jump, fall
            self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
            self.air_time += time.dt * .25 * self.gravity


    def input(self, key):
        if key == 'space':
            self.jump()


    def jump(self):
        if not self.grounded:
            return

        self.grounded = False
        self.animate_y(self.y+self.jump_height, self.jump_up_duration, resolution=int(1//time.dt), curve=curve.out_expo)
        invoke(self.start_fall, delay=self.fall_after)


    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False

    def land(self):
        # print('land')
        self.air_time = 0
        self.grounded = True


    def on_enable(self):
        mouse.locked = True
        self.cursor.enabled = True


    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False


