#include <QXmlStreamWriter>

#include "xmlformattedresults.h"
#include "floatarray.h"
#include "filedialogs.h"
#include "utilitydialog.h"

const int REAL_NUMBER_PRECISION = 8;

XMLFormattedResults::XMLFormattedResults( ReactionSchemeDiagram* pSchemeDiagram ) :
    scheme_diagram( pSchemeDiagram ),
    format_style( COMMA_DELIMITED ),
    separator( ',' )
{
    scheme = scheme_diagram->scheme();
    results = scheme->results();
    scheme3D = false;
}

XMLFormattedResults::XMLFormattedResults( FixedReactionSchemeDiagram* pSchemeDiagram ) :
    fixed_scheme_diagram( pSchemeDiagram ),
    format_style( COMMA_DELIMITED ),
    separator( ',' )
{
    scheme = fixed_scheme_diagram->scheme();
    results = scheme->results();
    scheme3D = true;
    num_rows = fixed_scheme_diagram->numRows();
    num_columns = fixed_scheme_diagram->numColumns();
    num_layers = fixed_scheme_diagram->numLayers();
}

void XMLFormattedResults::setOutputFile( QFile &file )
{
    xmlWriter.setDevice( &file );
}

void XMLFormattedResults::writeHeader()
{

    xmlWriter.setAutoFormatting(true);
    xmlWriter.writeStartDocument();
}

void XMLFormattedResults::formatRawData(QTextStream& data_in, FloatArray& data_array )
{
    for(UINTEGER32 i = 0; i < num_points; i++)
    {
        data_in << data_array[i];
        if( i != ( num_points - 1 ) )
        {
            data_in << separator;
        }
    }
}

void XMLFormattedResults::writeSchemeData()
{
    QString data_to_print;
    QTextStream data_in;
    FloatArray temp_array;




    data_in.setString( &data_to_print );

    data_in.setRealNumberNotation( QTextStream::SmartNotation );
    data_in.setRealNumberPrecision( REAL_NUMBER_PRECISION );

    num_compartments = results->numCompartments();
    num_species = results->numSpecies();
    num_points = results->numDataPts();

    xmlWriter.writeStartElement("scheme");
    xmlWriter.writeTextElement( "file", scheme->name() );
    xmlWriter.writeTextElement( "simulation_date", scheme->simulationStartDate().toString() );
    xmlWriter.writeTextElement( "file_date", QDateTime::currentDateTime().toString() );
    xmlWriter.writeTextElement( "simulation_type", QString::number( scheme->schemeType() ) );
    xmlWriter.writeTextElement( "num_points", QString::number( num_points ) );
    xmlWriter.writeTextElement( "num_compartments", QString::number( num_compartments ) );
    xmlWriter.writeTextElement( "num_species", QString::number( num_species ) );

    if(scheme3D)
    {
        xmlWriter.writeTextElement( "num_rows", QString::number( num_rows ) );
        xmlWriter.writeTextElement( "num_columns", QString::number( num_columns ) );
        xmlWriter.writeTextElement( "num_layers", QString::number( num_layers ) );
    }

    xmlWriter.writeStartElement("units");
    xmlWriter.writeTextElement("length", scheme->lengthUnitsAsStr() );
    xmlWriter.writeTextElement("volume", scheme->volumeUnitsAsStr() );
    xmlWriter.writeTextElement("pressure", scheme->pressureUnitsAsStr() );
    xmlWriter.writeTextElement("temperature", scheme->temperatureUnitsAsStr() );
    xmlWriter.writeTextElement("amount", scheme->amountUnitsAsStr() );

    // end units tag
    xmlWriter.writeEndElement();





    // Get time points, format using separator, and write to time xml element
    temp_array = results->GetElapsedTimeArray();
    formatRawData( data_in, temp_array );


    xmlWriter.writeTextElement( "time_points", data_to_print);
    data_in.flush();

}

void XMLFormattedResults::writeData()
{
    QString data_to_print;
    QTextStream data_in;
    FloatArray temp_array;

    data_in.setString( &data_to_print );

    data_in.setRealNumberNotation( QTextStream::SmartNotation );
    data_in.setRealNumberPrecision( REAL_NUMBER_PRECISION );

    if(scheme3D)
    {
          for( int column = 0; column < num_columns; column++ )
          {
              for( int row = 0; row < num_rows; row++ )
              {
                  for( int layer = 0; layer < num_layers; layer++ )
                  {

                      CompartmentObject* compartment = fixed_scheme_diagram->compartmentAt( row, column, layer );
                      int compt_obj_index = compartment->index();

                      xmlWriter.writeStartElement( "compartment" );
                      xmlWriter.writeTextElement( "description", compartment->name() );
                      xmlWriter.writeTextElement( "index", QString::number( compt_obj_index ) );

                      // output coordinates of compartment

                      xmlWriter.writeStartElement( "coordinates" );

                      xmlWriter.writeTextElement( "column", QString::number( column ) );
                      xmlWriter.writeTextElement( "row", QString::number( row ) );
                      xmlWriter.writeTextElement( "layer", QString::number( layer ) );

                      // close coordinates tag
                      xmlWriter.writeEndElement();

                      // output initial dimensions of compartment

                      xmlWriter.writeStartElement( "dimensions" );
                      xmlWriter.writeTextElement( "x_initial", compartment->xDimension() );
                      xmlWriter.writeTextElement( "y_initial", compartment->yDimension() );
                      xmlWriter.writeTextElement( "z_initial", compartment->zDimension() );

                      // close dimensions tag
                      xmlWriter.writeEndElement();

                      // get compartment state
                      CompartmentState* compartment_state = results->GetpComptState( compt_obj_index );

                      // Placeholder for electrochem data (have no models that use it to test)

                      // Format and output volume data
                      temp_array = compartment_state->GetVolumeArray();
                      formatRawData( data_in, temp_array );
                      xmlWriter.writeTextElement( "volume", data_to_print );

                      data_to_print.clear();
                      data_in.flush();

                      // Format and output pressure data
                      temp_array = compartment_state->GetPressureArray();
                      formatRawData( data_in, temp_array );
                      xmlWriter.writeTextElement( "pressure", data_to_print );

                      data_to_print.clear();
                      data_in.flush();

                      // Format and output temperature data
                      temp_array = compartment_state->GetTemperatureArray();
                      formatRawData( data_in, temp_array );
                      xmlWriter.writeTextElement( "temperature", data_to_print );

                      data_to_print.clear();
                      data_in.flush();

                      // Placeholder for electrochem

                      // Format and output species amount data for each species

                      for( unsigned int i = 0; i < num_species; i++ )
                      {
                          SPECIES_ID id = i + 1;
                          // Format species amounts, write tags for name
                          temp_array = compartment_state->GetAmounts( id );
                          formatRawData( data_in, temp_array );
                          xmlWriter.writeStartElement( "species" );
                          xmlWriter.writeTextElement( "name", scheme->speciesDatabase()->GetSpeciesDataByID( id ).GetName() );
                          xmlWriter.writeTextElement( "ID", QString::number( i + 1 ) );
                          xmlWriter.writeTextElement( "amount", data_to_print );

                          // End species tag
                          xmlWriter.writeEndElement();

                          data_to_print.clear();
                          data_in.flush();
                      }

                      // close compartment tag
                      xmlWriter.writeEndElement();
                  }
              }
          }
    }
    else
    {
        for( int compartment_index = 0; compartment_index < num_compartments; compartment_index++)
        {
            CompartmentObject* compartment = scheme->compartmentObjectFromIndex( compartment_index );
            xmlWriter.writeStartElement( "compartment" );
            xmlWriter.writeTextElement( "name", compartment->name() );
            xmlWriter.writeTextElement( "index", QString::number( compartment->index() ) );

            // close compartment tag
            xmlWriter.writeEndElement();



        }
    }

    // end scheme tag and write document end
    xmlWriter.writeEndElement();
    xmlWriter.writeEndDocument();
}

void XMLFormattedResults::writeResults()
{
    writeHeader();
    writeSchemeData();
    writeData();
}

void XMLFormattedResults::setDelimiter( enum TEXT_FORMAT_STYLE d )
{
    format_style = d;

    switch ( format_style )
    {
        case HTML_STYLE:
            separator = QChar( ' ' );
            break;

        case TAB_DELIMITED:
            separator = QChar( '\t' );
            break;

        case COMMA_DELIMITED:
            separator = QChar( ',' );
            break;

        case SPACE_DELIMITED:
            separator = QChar( ' ' );
            break;
    }

}

void XMLFormattedResults::openFileDialog()
{
    QString filename;
    QString format;

    if ( saveXMLFileDialog( filename, format ) )
    {
        QFile f( filename );

        if ( f.open( QFile::WriteOnly | QFile::Truncate ) )
        {
            setOutputFile( f );
            writeResults();
        }
        else
        {
            FileErrorDlg();
        }
    }

}
