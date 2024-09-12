<template>
    <div class="li-stat">
      <h1>Library Statistics</h1>
      <button @click="goToMainDashboard" class="main-dashboard-button">
      Main Dashboard
    </button>
      <div class="chart-container">
        <div class="bar-chart">
          <h2>Book Statistics</h2>
          <canvas ref="bookStatsChart"></canvas>
        </div>
        
        <div class="pie-chart">
          <h2>Section Distribution</h2>
          <canvas ref="sectionChart"></canvas>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Chart from 'chart.js/auto';
  
  export default {
    name: 'LiStat',
    data() {
      return {
        bookStats: {},
        sectionStats: {},
      };
    },
    mounted() {
      this.fetchStatistics();
    },
    methods: {
        goToMainDashboard() {
      const username = localStorage.getItem('username');
      this.$router.push({ name: 'UserDashboard', params: { username } });
    },
      async fetchStatistics() {
        try {
          const response = await fetch('http://localhost:5000/api/statistics1');
          const data = await response.json();
          this.bookStats = data.bookStats;
          this.sectionStats = data.sectionStats;
          this.createCharts();
        } catch (error) {
          console.error('Error fetching statistics:', error);
        }
      },
      createCharts() {
        this.createBookStatsChart();
        this.createSectionChart();
      },
      createBookStatsChart() {
        const ctx = this.$refs.bookStatsChart.getContext('2d');
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['Books Granted','Books Rejected','Pending Requests','Returned books'],
            datasets: [{
              label: 'Book Statistics',
              data: [
                this.bookStats.booksGranted,
                this.bookStats.booksRejected,
                this.bookStats.pendingRequests,
                this.bookStats.booksReturned,
              ],
              backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)'
              ],
              borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      },
      createSectionChart() {
        const ctx = this.$refs.sectionChart.getContext('2d');
        new Chart(ctx, {
          type: 'pie',
          data: {
            labels: Object.keys(this.sectionStats),
            datasets: [{
              data: Object.values(this.sectionStats),
              backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(75, 192, 192, 0.6)',
              ],
              borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(54, 162, 235, 1)',
              ],
              borderWidth: 1
            }]
          },
          options: {
            responsive: true
          }
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .li-stat{
    background-color: #EDE8F5;
    padding: 20px;
  }
  .main-dashboard-button {
  padding: 10px 20px;
  font-size: 16px;
  color: white;
  background-color: #7091E6;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  position: absolute; /* Position the button absolutely */
  top: 25px; /* Distance from the top */
  right: 25px; /* Distance from the right */
  }
  
  .main-dashboard-button:hover {
  background-color: #5671b5;
  }
  
  
  .li-stat {
    padding: 20px;
  }
  
  .chart-container {
    color: #3d52a0;
    display: flex;
    justify-content: space-around;
    margin-top: 20px;
  }
  
  .bar-chart, .pie-chart {
    width: 45%;
  }
  </style>