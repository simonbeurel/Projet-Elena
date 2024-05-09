from flask import Flask, send_from_directory
from flask import render_template

from backend import util, graph_builder


app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('hello.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/game/<namePlayer1>/<namePlayer2>')
def game_page(namePlayer1, namePlayer2):
    elo_1 = util.retrieve_player_id_from_lastname(namePlayer1)
    full_name_1 = util.retrieve_player_fullname_from_id(elo_1)

    elo_2 = util.retrieve_player_id_from_lastname(namePlayer2)
    full_name_2 = util.retrieve_player_fullname_from_id(elo_2)


    result = util.retrieve_player_statsAce(full_name_1, elo_1)
    graph_builder.build_graph_aces_last_10_matches(result[0][::-1], full_name_1)
    graph_builder.build_graph_aces_against_ranked_receiver(result[0][::-1], result[2][::-1], full_name_1, str(namePlayer2).lower())

    result = util.retrieve_player_statsAce(full_name_2, elo_2)
    graph_builder.build_graph_receive_stats_last_10_matches(result[1][::-1], full_name_2)
    graph_builder.build_graph_aces_against_ranked_server(result[1][::-1], result[2][::-1], full_name_2, str(namePlayer1).lower())

    return render_template('game.html',
                           namePlayer1=full_name_1,
                           namePlayer2=full_name_2)






if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000 ,debug=True)
