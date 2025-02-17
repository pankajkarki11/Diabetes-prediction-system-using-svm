$(document).ready(function() {
  // Open modal for steps
  $('#addStepsBtn').click(function() {
      $('#modal1').show(); // Show modal
  });

  // Open modal for calories
  $('#addCaloriesBtn').click(function() {
      $('#modal2').show(); // Show modal
  });

  // Close modal for steps
  $('#closeModalBtn1').click(function() {
      $('#modal1').hide(); // Hide modal
  });

  // Close modal for calories
  $('#closeModalBtn2').click(function() {
      $('#modal2').hide(); // Hide modal
  });

  // Submit form for adding steps
  $('#stepsForm').submit(function(e) {
      e.preventDefault();
      const steps = $('#numberOfSteps').val();  // Get number of steps value

      if (isNaN(steps) || steps <= 0) {
          alert('Please enter a valid number of steps.');
          return;
      }

      $.ajax({
          type: 'POST',
          url: '/track/update_steps/', // Ensure this matches your view's URL
          data: {
              'steps': steps,
              'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val() // CSRF token
          },
          success: function(response) {
              if (response.plot_data) {
                  $('.image-container img').attr('src', 'data:image/png;base64,' + response.plot_data);
                  $('.message').text(response.message);  // Display success message
              }
          },
          error: function(xhr, status, error) {
              alert('Error: ' + xhr.responseJSON.error);
          }
      });
      $('#modal1').hide(); // Hide modal after submit
  });

  // Submit form for adding calories
  $('#caloriesForm').submit(function(e) {
      e.preventDefault();
      const caloriesBurned = $('#Calories-burned').val();
      const caloriesIntake = $('#Calories-intake').val();

      if (isNaN(caloriesBurned) || isNaN(caloriesIntake)) {
          alert('Please enter valid numbers for calories.');
          return;
      }

      $.ajax({
          type: 'POST',
          url: '/track/update_calories/',  // Ensure this matches your view's URL
          data: {
              'calories_burned': caloriesBurned,
              'calories_intake': caloriesIntake,
              'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()  // CSRF token
          },
          success: function(response) {
              if (response.plot_data) {
                  $('.image-container img').attr('src', 'data:image/png;base64,' + response.plot_data);
                  $('.message').text(response.message);  // Display success message
              }
          },
          error: function(xhr, status, error) {
              alert('Error: ' + xhr.responseJSON.error);
          }
      });
      $('#modal2').hide(); // Hide modal after submit
  });
});
