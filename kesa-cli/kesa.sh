#!/bin/bash
gum style --border normal --margin "1" --padding "1 2" --border-foreground 212 "Hello, there! I'm $(gum style --foreground 212 'Kesa!')."

#####################functions#########################
kesa_cli_select_compute(){
  echo "$(gum style --foreground 90 'are you processing using this computer or a remote server?')"
  COMPUTE=$(gum choose --limit 1 "Local" "Remote")
  echo "Processing: $COMPUTE"
}
kesa_cli_config_params (){
  CONFIGWHAT=$(gum choose --limit 1 "CREATE CONFIG" "ADDRESS" "AUTO-LABEL" "SELECT DEVICE" "CONFIG SUMMARY")
  if [ "$CONFIGWHAT" = "ADDRESS" ]; then
    kesa_cli_config_add_remote_ADDRESS
    kesa_cli_welcome
  elif [ "$CONFIGWHAT" = "CREATE CONFIG" ]; then
    kesa_cli_config_create
    kesa_cli_welcome
  elif [ "$CONFIGWHAT" = "AUTO-LABEL" ]; then
    kesa_cli_config_add_autolabel
    kesa_cli_welcome
  elif [ "$CONFIGWHAT" = "SELECT DEVICE" ]; then
    kesa_cli_config_add_device
    kesa_cli_welcome   
  elif [ "$CONFIGWHAT" = "CONFIG SUMMARY" ]; then
    kesa_cli_config_print
    kesa_cli_welcome   
  fi 
}

kesa_cli_config_create() {
  echo "$(gum style --foreground 90 'create cfg.ini from scratch')"
  kesa_cli_config_add_remote_ADDRESS
  kesa_cli_config_add_autolabel
  kesa_cli_config_add_device
}

kesa_cli_config_add_remote_ADDRESS () {
  ADDRESS=$(gum input --placeholder "please enter remote address, if you are processing locally, you can press [ENTER]")
}
kesa_cli_config_add_autolabel () {
  CONFIDENCE=$(gum input --placeholder "confidence: please enter a float from 0-1 i.e 0.89")
  IOU=$(gum input --placeholder "IOU: please enter a float from 0-1 i.e 0.89")
}

kesa_cli_config_add_device () {
  DEVICE=$(gum input --placeholder "please enter 'cpu' for cpu or device index (0,1,2,3..) to select a CUDA device")
}

kesa_cli_config_print () {
  clear;
  echo "$(gum style --foreground 255 --background 128 'Configuration Summary')"
}

kesa_cli_welcome () {
  echo "$(gum style --foreground 56 'What would you like to do?')"
  LABEL="Label"; CONVERT="Convert"; CONFIGURE="Configure"; EXIT="Exit";
  TASK=$(gum choose --item.foreground 78 "$LABEL" "$CONVERT" "$CONFIGURE" "$EXIT")
  echo "Task: $(gum style --foreground 212 "$TASK")"
}
########################################################

kesa_cli_select_compute
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
  kesa_cli_config_params
fi
