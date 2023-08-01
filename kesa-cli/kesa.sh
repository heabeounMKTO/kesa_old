#!/bin/sh
gum style --border normal --margin "1" --padding "1 2" --border-foreground 212 "Hello, there! I'm $(gum style --foreground 212 'Kesa!')."
kesa_cli_welcome () {
  echo "$(gum style --foreground 56 'What would you like to do?')"

  LABEL="Label"; CONVERT="Convert"; CONFIGURE="Configure"; EXIT="Exit";
  TASK=$(gum choose --item.foreground 78 "$LABEL" "$CONVERT" "$CONFIGURE" "$EXIT")
  echo "Task: $(gum style --foreground 212 "$TASK")"
}

kesa_cli_welcome

if [ "$TASK" = "$EXIT" ]; then
  EXITCONF=$(gum confirm "are we saying goodbye?") 
  echo "$EXITCONF"
elif [ "$TASK" = "$LABEL" ]; then
  DATASET_DIR=$(gum input --placeholder "Can you tell me where the dataset is?")
  AUGMENT=$(gum input --placeholder "want augmentations on your data? (please enter 0 for no augmentations)")
  YOLO="YOLOTXT"; COCO="COCO (not available yet)"; PASCAL="PascalVOC (not available yet)";
  TARGET_FMT=$(gum choose --cursor "*" --cursor-prefix "[ ] " --selected-prefix "[*] " --limit 1 "$YOLO" "$COCO" "$PASCAL")
  clear; gum style --foreground 56 'Summary:'
  echo "Working Directory: $(gum style --foreground 212 "$DATASET_DIR")"
  echo "Augmentations: $(gum style --foreground 212 "$AUGMENT")"
  echo "Target Format: $(gum style --foreground 212 "$TARGET_FMT")"
  gum confirm "are you happy with the current config?" && echo "starting "$TASK"" || echo "changign"
elif [ "$TASK" = "$CONFIGURE" ]; then
  nano cfg.ini 
fi
