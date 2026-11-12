# idk

A platforming playground Creation for Other5: maps `SodaCity`, `m` and `LowerSector_Mod`, the player
(`Player/BP_Tabholder`, the Countess on a template mannequin) and its platforming Blueprints. It needs Other5ThirdPerson
and Other5Characters.

## What's real here, and what's a stand-in
- **Other5's own:** the maps and their placed actors, the player and Blueprints, and `PAL_idk`.
- **Stand-ins** for art that comes from Fab, because its licence doesn't let anyone share the source files:
  - the **Lower Sector Building Kit** by tunami3d (free on Fab): grey boxes and plain materials at the kit's paths, so
    the maps load and play with the city blocked out;
  - the **Megaplant Library** cherry trees (free on Fab; the real ones need the experimental Procedural Vegetation
    Editor plugin): small one-bone skeletal boxes.

  `StandIns.json` lists each one and where the real asset comes from.

To get the real look, use **Tools > Other5 Setup** in the Other5 Creator. It walks you through adding these Fab
listings to your own Epic account and bringing them into your project, then puts the real assets in place of the
stand-ins. Your Creation's paks then ship them, cooked, under your own licence. The real files live in your **Other5
library** (by default a folder `Other5Library` next to your project folder), never in this repository.
