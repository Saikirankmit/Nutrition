function selectPlan(plan) {
          const details = {
            weightLoss: {
              title: "Weight Loss Plan",
              content: "A low-calorie diet focused on creating a calorie deficit for fat loss."
            },
            weightGain: {
              title: "Weight Gain Plan",
              content: "A high-calorie diet designed to help you increase healthy body weight."
            },
            fitness: {
              title: "Fitness Plan",
              content: "A low-fat diet optimized for lean body maintenance and overall fitness."
            },
            muscle: {
              title: "Muscle Building Plan",
              content: "A high-protein diet tailored to support muscle growth and recovery."
            }
          };
        
          const planData = details[plan];
          const container = document.getElementById("planDetails");
        
          container.innerHTML = `
            <h3>${planData.title}</h3>
            <p>${planData.content}</p>
            <p><strong>Selected Plan:</strong> ${plan}</p>
          `;
        
          localStorage.setItem('nutrifyPlan', plan);
          container.style.display = 'block';
        }
        