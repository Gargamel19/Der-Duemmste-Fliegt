function reload_urls() {
    const btn_player0_url = document.getElementById("player_0_url").value
    const btn_player1_url = document.getElementById("player_1_url").value
    const btn_player2_url = document.getElementById("player_2_url").value
    const btn_player3_url = document.getElementById("player_3_url").value
    const btn_player4_url = document.getElementById("player_4_url").value
    const btn_host_url = document.getElementById("host_url").value

    if(btn_player0_url!==document.getElementById("player_0_cam").src){
        document.getElementById("player_0_cam").src = btn_player0_url
    }
    if(btn_player1_url!==document.getElementById("player_1_cam").src){
        document.getElementById("player_1_cam").src = btn_player1_url
    }
    if(btn_player2_url!==document.getElementById("player_2_cam").src){
        document.getElementById("player_2_cam").src = btn_player2_url
    }
    if(btn_player3_url!==document.getElementById("player_3_cam").src){
        document.getElementById("player_3_cam").src = btn_player3_url
    }
    if(btn_player4_url!==document.getElementById("player_4_cam").src){
        document.getElementById("player_4_cam").src = btn_player4_url
    }
    if(btn_host_url!==document.getElementById("host_url").src){
        document.getElementById("host_cam").src = btn_host_url
    }
}

function reload_all_urls() {
    const btn_player0_url = document.getElementById("player_0_url").value
    const btn_player1_url = document.getElementById("player_1_url").value
    const btn_player2_url = document.getElementById("player_2_url").value
    const btn_player3_url = document.getElementById("player_3_url").value
    const btn_player4_url = document.getElementById("player_4_url").value
    const btn_host_url = document.getElementById("host_url").value

    document.getElementById("player_0_cam").src = btn_player0_url
    document.getElementById("player_1_cam").src = btn_player1_url
    document.getElementById("player_2_cam").src = btn_player2_url
    document.getElementById("player_3_cam").src = btn_player3_url
    document.getElementById("player_4_cam").src = btn_player4_url
    document.getElementById("host_cam").src = btn_host_url
}

