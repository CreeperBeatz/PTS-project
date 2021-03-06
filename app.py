# System imports
import io

# Dependency imports
from quart import Quart, request, Response
from quart_cors import cors
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Self imports
from template_engine import correlation_template, generalized_analysis_template, main_menu_template
from file_manager import get_activity_per_user, create_json_files, load_grade_to_visited_courses
from math_analyzer import correlation_analysis

application = Quart(__name__, )
application = cors(
    application,
    allow_origin="*",
    allow_headers=['Content-Type', ],
    allow_methods=['GET'],
)

# Create JSON files for faster request response
application.before_serving(create_json_files)

# ###### API REQUEST HANDLERS ######


@application.route('/', methods=['GET', 'POST'], )
async def main_menu():
    """
    Function for getting main menu
    """
    return main_menu_template(), 200


@application.route('/generalized_analysis', methods=['GET', ], )
async def get_generalized_analysis():
    """
    Get table of user_ids and activities

    if user_id == None, all users are shown

    if user_id is valid, show only for user
    """
    user_id = request.args.get('id', type=int)

    return generalized_analysis_template(get_activity_per_user(user_id)), 200


@application.route('/correlation_analysis', methods=['GET', ], )
async def get_correlation_analysis():
    """
    get correlation analysis

    """
    return correlation_template(correlation_analysis(load_grade_to_visited_courses())), 200


@application.route('/correlation_picture', methods=['GET'])
async def get_correlation_picture():
    """
    Get a dinamically generated picture of the correlation graph
    """
    dataset = load_grade_to_visited_courses()

    def create_figure():
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        xs = [row['times_visited_courses'] for row in dataset]
        ys = [row['grade'] for row in dataset]
        axis.scatter(xs, ys)
        axis.set_title("Correlation Graph")
        axis.set_xlabel("Number of times lectures checked")
        axis.set_ylabel("Grade")
        return fig
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

# Run the server
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80, debug=True, )


# Put anything that you want to start from hypercorn master process here
def on_starting(_server):
    pass
