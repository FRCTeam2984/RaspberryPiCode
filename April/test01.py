#Camera Calibration Parameters
camera_info = load_camera_information()

#Scene Setup
tags=Tag()
tags.add_tag(tag_id,x,y,z,theta_x,theta_y,theta_z)

### Detector
detector = Detector(families="tagStandard41h12",nthreads=4)
#Main Loop
with PiCamera() as camera:
  stream = Stream(tags,camera_info,detector)
  try:
    # Start recording frames to the stream object
    camera.start_recording(stream, format='yuv')
    t0 = time()

    while True:
      camera.wait_recording()
      # If the time limit is reached, end the recording
      if ((time() - t0) > MAX_TIME):
          camera.stop_recording()
          break