WALL_THICKNESS = 2.5;
BASE_HEIGHT = 20;
False = false;
True = true;
$fa = 36;

module tile (width=12, u=false, r=false, d=false, l=false) {
    wall_height = 0.55 * width + 1;
    
    render() difference() {
        render() union() {
            // base
            cube([width+(2*WALL_THICKNESS), width+(2*WALL_THICKNESS), BASE_HEIGHT]);
            
            // walls
            union() {
                translate([0, width+WALL_THICKNESS, BASE_HEIGHT-1]) {
                    cube([width+(2*WALL_THICKNESS), WALL_THICKNESS, wall_height]);
                }
                translate([width+WALL_THICKNESS, 0, BASE_HEIGHT-1]) {
                    cube([WALL_THICKNESS, width+(2*WALL_THICKNESS), wall_height]);
                }
                translate([0,0,BASE_HEIGHT-1]) {
                    cube([width+(2*WALL_THICKNESS), WALL_THICKNESS, wall_height]);
                }
                translate([0,0,BASE_HEIGHT-1]) {
                    cube([WALL_THICKNESS, width+(2*WALL_THICKNESS), wall_height]);
                }
            }
        }

        // minus track curve
        render() union() {
            if (!(!u&&!d) && !(!r&&!l)) {
                translate([WALL_THICKNESS+(width/2), WALL_THICKNESS+(width/2), BASE_HEIGHT]) {
                    sphere(width/2);
                }
            }
            if (!u) {
                translate([WALL_THICKNESS+(width/2), WALL_THICKNESS+(width/2)-0.001, BASE_HEIGHT]) {
                    rotate([-90,0,0]) {
                        render() union() {
                            cylinder(WALL_THICKNESS+width/2+2, width/2, width/2);
                            translate([0, -(width/2)+1, (WALL_THICKNESS+width/2+2)/2]) {
                                cube([width-0.001, width-0.001, WALL_THICKNESS+width/2+2], true);
                            }
                        }
                    }
                }
            }
            if (!r) {
                translate([WALL_THICKNESS+(width/2)-0.001, WALL_THICKNESS+(width/2), BASE_HEIGHT]) {
                    rotate([-90,0,-90]) {
                        render() union() {
                            cylinder(WALL_THICKNESS+width/2+2, width/2, width/2);
                            translate([0, -(width/2)+1, (WALL_THICKNESS+width/2+2)/2]) {
                                cube([width-0.001, width-0.001, WALL_THICKNESS+width/2+2], true);
                            }
                        }
                    }
                }
            }
            if (!d) {
                translate([WALL_THICKNESS+(width/2), WALL_THICKNESS+(width/2)+0.001, BASE_HEIGHT]) {
                    rotate([90,0,0]) {
                        render() union() {
                            cylinder(WALL_THICKNESS+width/2+2, width/2, width/2);
                            translate([0, (width/2)-1, (WALL_THICKNESS+width/2+2)/2]) {
                                cube([width-0.001, width-0.001, WALL_THICKNESS+width/2+2], true);
                            }
                        }
                    }
                }
            }
            if (!l) {
                translate([WALL_THICKNESS+(width/2)+0.001, WALL_THICKNESS+(width/2), BASE_HEIGHT]) {
                    rotate([90,0,-90]) {
                        render() union() {
                            cylinder(WALL_THICKNESS+width/2+2, width/2, width/2);
                            translate([0, (width/2)-1, (WALL_THICKNESS+width/2+2)/2]) {
                                cube([width-0.001, width-0.001, WALL_THICKNESS+width/2+2], true);
                            }
                        }
                    }
                }
            }
        }
    }
}