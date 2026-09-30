extends Node2D

@onready var dialog: Control = $CanvasLayer/DialogPanel
@onready var hint: Label = $CanvasLayer/Hint

func _ready() -> void:
	hint.text = "WASD déplacer · E parler au PNJ (mode mock)"
	for npc in get_tree().get_nodes_in_group("npc"):
		if npc.has_signal("interacted"):
			npc.interacted.connect(_on_npc_interacted)

func _on_npc_interacted(npc_id: String, display_name: String) -> void:
	dialog.open_for(npc_id, display_name)
