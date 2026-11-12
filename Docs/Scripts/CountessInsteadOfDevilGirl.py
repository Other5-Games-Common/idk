# idk: the player (BP_Tabholder) becomes the Countess instead of Devil Girl (a Fab pack by AlexN that was free and is
# now paid). The character's own mesh is the template Quinn, which ABP_Quinn animates as before (unseen); an
# Other5CharacterSkins component retargets that pose onto the Countess (Other5Characters, free on Fab as Paragon:
# Countess). The jump effect (Devil Girl's JetsExplosion) becomes the engine's Niagara SimpleExplosion template.
# Rerunnable. Run headless or in the editor: py "<this file>". Afterwards delete Content/DevilGirl.
import unreal

def log(s):
	unreal.log("CountessSwap: " + s)

R = unreal.AssetRegistryHelpers.get_asset_registry()
R.search_all_assets(True)
Lib = unreal.EditorAssetLibrary
Sub = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
SubLib = unreal.SubobjectDataBlueprintFunctionLibrary

BP = unreal.load_asset("/idk/Player/BP_Tabholder.BP_Tabholder")
Quinn = unreal.load_asset("/Other5ThirdPerson/Characters/Mannequins/Meshes/SKM_Quinn.SKM_Quinn")
Countess = unreal.load_asset("/Other5Characters/Countess/Characters/Heroes/Countess/Meshes/SM_Countess.SM_Countess")
Retargeter = unreal.load_asset("/Other5Characters/Countess/Rigs/RTG_Mannequin_Countess.RTG_Mannequin_Countess")
Explosion = unreal.load_asset("/Niagara/DefaultAssets/Templates/Systems/SimpleExplosion.SimpleExplosion")
for Name, Asset in (("BP_Tabholder", BP), ("SKM_Quinn", Quinn), ("SM_Countess", Countess), ("RTG_Mannequin_Countess", Retargeter), ("SimpleExplosion", Explosion)):
	if not Asset:
		raise RuntimeError("missing " + Name)

# 1. The jump effect: everything that used JetsExplosion uses the engine's SimpleExplosion.
Jets = unreal.load_asset("/idk/DevilGirl/JetsExplosion.JetsExplosion")
if Jets:
	log("JetsExplosion -> SimpleExplosion: %s" % Lib.consolidate_assets(Explosion, [Jets]))

# 2. The character's own mesh: the template Quinn (ABP_Quinn animates it; the Countess skin hides it).
Cdo = unreal.get_default_object(BP.generated_class())
MeshComp = Cdo.get_editor_property("mesh")
MeshComp.set_skeletal_mesh_asset(Quinn)
log("mesh = %s" % MeshComp.get_skeletal_mesh_asset().get_path_name())

# 3. The Countess skin.
def Find(Name):
	for H in Sub.k2_gather_subobject_data_for_blueprint(BP):
		O = SubLib.get_object(SubLib.get_data(H))
		if O and O.get_name().replace("_GEN_VARIABLE", "") == Name:
			return O
	return None

Skins = Find("CharacterSkins")
if not Skins:
	Root = Sub.k2_gather_subobject_data_for_blueprint(BP)[0]
	Handle, Fail = Sub.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=Root, new_class=unreal.Other5CharacterSkins, blueprint_context=BP))
	Sub.rename_subobject(Handle, unreal.Text("CharacterSkins"))
	Skins = SubLib.get_object(SubLib.get_data(Handle))
Skin = unreal.Other5CharacterSkin()
Skin.set_editor_property("display_name", unreal.Text("Countess"))
Skin.set_editor_property("retargeted_mesh", Countess)
Skin.set_editor_property("retargeter", Retargeter)
Skin.set_editor_property("hidden_material_slots", [unreal.Name("M03_Swords_holster")])
Skins.set_editor_property("skins", [Skin])
Skins.set_editor_property("default_skin", 0)
log("skins = Countess")

unreal.BlueprintEditorLibrary.compile_blueprint(BP)
Lib.save_loaded_asset(BP, only_if_is_dirty=False)

# 4. The label: nothing under DevilGirl any more.
Pal = unreal.load_asset("/idk/PAL_idk.PAL_idk")
if Pal:
	Rules = Pal.get_editor_property("explicit_assets")
	Kept = [A for A in Rules if A and not A.get_path_name().startswith("/idk/DevilGirl")]
	if len(Kept) != len(Rules):
		Pal.set_editor_property("explicit_assets", Kept)
		Lib.save_loaded_asset(Pal, only_if_is_dirty=False)
		log("PAL_idk: %d DevilGirl entries removed" % (len(Rules) - len(Kept)))

# 5. Read back.
BP2 = unreal.load_asset("/idk/Player/BP_Tabholder.BP_Tabholder")
Cdo2 = unreal.get_default_object(BP2.generated_class())
log("check: mesh %s; skins %s" % (Cdo2.get_editor_property("mesh").get_skeletal_mesh_asset().get_name(),
	[S.get_editor_property("display_name") for S in Find("CharacterSkins").get_editor_property("skins")]))
Deps = [str(D) for D in R.get_dependencies("/idk/Player/BP_Tabholder", unreal.AssetRegistryDependencyOptions()) if "DevilGirl" in str(D)]
log("check: DevilGirl dependencies left: %s" % Deps)
