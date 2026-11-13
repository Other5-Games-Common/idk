# idk: Cozy Nature trees in place of the 7 Megaplants Yoshino Cherry trees in map m (skeletal mesh actors), so idk
# no longer needs Megaplants or Epic's experimental Procedural Vegetation Editor plugin. Same transforms; static meshes.
import unreal
unreal.EditorLoadingAndSavingUtils.load_map("/idk/Maps/m")
Sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
R = unreal.AssetRegistryHelpers.get_asset_registry()
R.search_all_assets(True)
Pkgs = ["/idk/__ExternalActors__/Maps/m/0/QL/SE8ZNTEKK81VE49MGOXRJR", "/idk/__ExternalActors__/Maps/m/4/SD/DRQ722SE8AC5TI2XK96YIX", "/idk/__ExternalActors__/Maps/m/6/YY/N5YB3YND5F9BYMGHDSAZNS", "/idk/__ExternalActors__/Maps/m/7/E5/5VM0G5P5XZ9GREV7THGKRV", "/idk/__ExternalActors__/Maps/m/C/0C/IQMWPS48ISILIG8IUBPN2Q", "/idk/__ExternalActors__/Maps/m/D/9D/2DOGHTTJ4NPJ64DH6V2JOE", "/idk/__ExternalActors__/Maps/m/E/65/JQIEVMID2TUOG66L3XBR30"]
Letters = dict(zip(Pkgs, "DDABBCA"))  # from each package's leftover skeleton import (idk#1 saved them without a mesh)
Actors = [(D.get_asset(), Letters[P]) for P in Pkgs for D in R.get_assets_by_package_name(P, False)]
Pick = {"A": "SM_TreeOak01", "B": "SM_TreeOak02", "C": "SM_TreeBirch01", "D": "SM_TreeOak03"}
Done = []
for A, Letter in [x for x in Actors if x[0]]:
	Mesh = unreal.load_asset("/Other5ForestBiome_Minimal/CozyNature/Meshes/Trees/%s.%s" % (Pick.get(Letter, "SM_TreeOak01"), Pick.get(Letter, "SM_TreeOak01")))
	T = A.get_actor_transform()
	New = Sub.spawn_actor_from_class(unreal.StaticMeshActor, T.translation, T.rotation.rotator())
	New.set_actor_scale3d(T.scale3d)
	New.static_mesh_component.set_static_mesh(Mesh)
	New.set_actor_label("CozyTree_" + A.get_actor_label())
	Done.append(A.get_actor_label())
	Sub.destroy_actor(A)
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
open(r"F:/HomeDev/Other5Public/_State/idk/CherryToCozy.txt", "w").write("replaced %d: %s\n" % (len(Done), ", ".join(Done)))
