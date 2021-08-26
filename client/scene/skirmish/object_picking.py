from panda3d.core import CollisionNode, GeomNode, CollisionRay, CollisionTraverser, CollisionHandlerQueue
import core


# noinspection PyArgumentList
class ObjectPicking:
    def __init__(self, skirmish):
        self.skirmish = skirmish
        self.traverse_node = skirmish.node_3d
        self.picked = None

        self.collision_traverser = CollisionTraverser()
        self.collision_handler = CollisionHandlerQueue()

        self.picker_node = CollisionNode("mouse ray")
        self.picker_node.set_from_collide_mask(GeomNode.get_default_collide_mask())
        self.picker_node_path = core.instance.camera.attach_new_node(self.picker_node)
        self.picker_ray = CollisionRay()
        self.picker_node.add_solid(self.picker_ray)
        self.collision_traverser.add_collider(self.picker_node_path, self.collision_handler)

    def find_pickable(self):
        if core.instance.mouseWatcherNode.has_mouse():
            mouse_pos = core.instance.mouseWatcherNode.get_mouse()
            self.picker_ray.set_from_lens(core.instance.camNode, mouse_pos.get_x(), mouse_pos.get_y())
            self.collision_traverser.traverse(self.traverse_node)
            if self.collision_handler.get_num_entries() > 0:
                self.collision_handler.sort_entries()
                picked = self.collision_handler.get_entry(0).get_into_node_path()
                picked = picked.find_net_tag('id')
                if not picked.is_empty():
                    for player in self.skirmish.other_players:
                        if picked.get_tag('id') == player.get_tag('id'):
                            self.picked = player
                else:
                    self.picked = None
            else:
                self.picked = None

    def pick(self):
        self.skirmish.player.target = self.picked

