WALL_THICKNESS = 2.5;
BASE_HEIGHT = 20;
False = false;
True = true;

module tile (width=12, u=false, r=false, d=false, l=false) {
    wall_height = width * 1.5;

    union() {
        // base
        cube([width+(2*WALL_THICKNESS), width+(2*WALL_THICKNESS), BASE_HEIGHT]);
        
        // walls
        union() {
            if (u) {
                translate([0, width+WALL_THICKNESS, BASE_HEIGHT-1]) {
                    cube([width+(2*WALL_THICKNESS), WALL_THICKNESS, wall_height]);
                }
            }
            if (r) {
                translate([width+WALL_THICKNESS, 0, BASE_HEIGHT-1]) {
                    cube([WALL_THICKNESS, width+(2*WALL_THICKNESS), wall_height]);
                }
            }
            if (d) {
                translate([0,0,BASE_HEIGHT-1]) {
                    cube([width+(2*WALL_THICKNESS), WALL_THICKNESS, wall_height]);
                }
            }
            if (l) {
                translate([0,0,BASE_HEIGHT-1]) {
                    cube([WALL_THICKNESS, width+(2*WALL_THICKNESS), wall_height]);
                }
            }
        }
    }
}